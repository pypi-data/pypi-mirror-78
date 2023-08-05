#!/usr/bin/env python3

import logging
import os
import sys
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pprint import pprint  # noqa: W0611
from string import Template

import strictyaml
from box import Box

from .engine import ETLEngine
from .node import Node, PriorityRegistry
from .pipe import PipeRef
from .utils import isdict, islist, isstr

_l = logging.getLogger(__name__)


class Workflow:
    def __init__(self, source, settings=None):
        self.settings = Box(settings or {})
        self.read(source)
        self.app = None

    def read(self, source):
        """Load workflow from definition source (file path or string)."""
        self.source = source
        if source == '-':
            source = sys.stdin.read()
        elif isdict(source):
            pass  # TODO
        else:
            try:
                params = os.environ.copy()
                params.update(self.settings.params)
                source = Template(Path(source).read_text()).substitute(params)
            except FileNotFoundError:
                self.source = None
            except KeyError as e:
                raise ConfigurationException(
                    f'Missing environment variable "{e.args[0]}" (needed by {source})')

        self.definition = self.expand(Box(strictyaml.load(source).data, box_dots=True))

    __MISSING__ = object()

    def expand(self, settings, element=__MISSING__, seen=None):
        """Recursively expand all "<use>" references."""
        if element is self.__MISSING__:
            element = settings
        if seen is None:
            seen = set()
        if islist(element):
            return type(element)(self.expand(settings, e, seen=seen) for e in element)

        elif isdict(element):
            useref = element.pop('<use>', None)
            if useref:
                # if useref in seen:
                #     raise ConfigurationException(f'Circular reference detected: {useref}')

                seen.add(useref)
                try:
                    useref = type(element)(settings[useref].to_dict())
                except KeyError:
                    raise ConfigurationException(f'Reference "{useref}" not found')

                useref.merge_update(element)
                element = useref
            return type(element)((k, self.expand(settings, e, seen=seen))
                                 for k, e in element.items())

        return element

    def load(self):
        _l.info(f'Loading workflow from {self.source}')
        if self.app:
            raise RuntimeError('Workflow has already been loaded')

        self.app = Box(self.definition.to_dict(), box_dots=True)
        self.configure()
        self.build()

    def configure(self):
        """Locate and configure components."""
        _l.debug('Configuring workflow')
        # pprint(self.app)
        for wname, workflow in self.app.workflows.items():
            # print(f'workflow: {wname}')
            for nname, node in workflow.items():
                node.workflow = wname
                node.key = f'{wname}.{nname}'
                # print(f'  node: {node.key}')
                self._configure_node(node)
                for msgbox in ('inbox', 'outbox'):
                    self._configure_pipes(node, msgbox)
        for wname, workflow in self.app.workflows.items():
            # print(f'workflow: {wname}')
            for node in workflow.values():
                for msgbox in ('inbox', 'outbox'):
                    self._configure_connections(node, msgbox)
        # pprint(self.app)
        # import sys; sys.exit()

    def _configure_node(self, node):
        try:
            # if node.component == 'il.etl.components.local:LocalFileTreeX':
            #     import pudb; pudb.set_trace()
            node.component = resolve(node.component)
            # if component:
            #     node.component = component
            # else:
            #     raise ConfigurationException(f'')
        except:
            errmsg = f'Failed to import node "{node.get("component")}" (needed by {node.key})'
            _l.exception(errmsg)
            raise ConfigurationException(errmsg)

    def _configure_pipes(self, node, msgbox):
        # _l.debug(f'  * {msgbox}: {node.key}')

        # Get default channels from class, if any.
        defaults = getattr(node.component, msgbox.upper(), dict())
        if defaults:
            if islist(defaults):
                defaults = dict((c, None) for c in defaults)
            elif not isdict(defaults):
                raise ConfigurationException(
                    f'Default channels for {node.component} misconfigured')

        # Get channels from configured in definition.
        defined_channels = node.get(msgbox, {})
        ischannel = lambda v: isstr(v) or (isdict(v) and ('node' in v or 'component' in v))
        if isstr(defined_channels) and defined_channels.startswith('<'):
            return  # reference will be later resolved in _configure_connections()

        # Expand shortened configuration structure, if relevant.
        channels = Box(defaults)
        if ischannel(defined_channels):
            channels.update(default=defined_channels)
        else:
            channels.update(**defined_channels)
        if not channels:
            channels.update(default=None)
        # print(' mb 1', node.key, msgbox, channels)

        # Resolve pipe specs to classes.
        for name, spec in channels.items():
            channel = Box()
            if not spec:
                spec = 'pipekit.pipe:QueuePipe'
            if isstr(spec):
                # if spec == '<void>':
                #     spec = 'pipekit.pipe:NullPipe'
                if spec.startswith('<'):
                    channel.node = spec.strip('< ')
                else:
                    channel.component = spec
            elif isdict(spec):
                channel.update(spec)
            else:
                raise ConfigurationException(
                    f'Incorrect {msgbox} configuration for node {node.key}')

            if 'component' in channel:
                channel.component = resolve(channel.component)
            channels[name] = channel

        # print(' mb 2', channels)
        node[msgbox] = channels
        # _l.debug(f'  ** {msgbox}: {node.key}')

    def _configure_connections(self, node, msgbox):
        # _l.debug(f'  * {msgbox}: {node.key}')

        # Import all channels from peer node, if configured in.
        defined_channels = node.get(msgbox, {})
        if isstr(defined_channels) and defined_channels.startswith('<'):
            spec = defined_channels.strip('< ')
            peer_node, _ = self.peer_node(spec, node)
            peer_msgbox = 'outbox' if msgbox == 'inbox' else 'inbox'
            # _l.debug(f'  ** new PipeRefs: {node.key} < {peer_node.key}.{peer_msgbox}')
            channels = Box((c, PipeRef(peer_node, peer_msgbox, c))
                           for c in getattr(peer_node, peer_msgbox))

            # print(' mb 2', channels)
            node[msgbox] = channels
        # _l.debug(f'  ** {msgbox}: {node.key}')

    def build(self):
        """Instantiate and wire up nodes and pipes."""
        _l.debug('Instantiating workflow')
        self._node_backlog = dict()
        for workflow in self.app.workflows.values():
            for _, node in workflow.items():
                self._node_backlog[node.key] = node
        for node in list(self._node_backlog.values()):
            try:
                _l.info(f'Creating node {node.key}')
                self.make_node(node)
            except Exception:
                _l.exception(f'Error while instantiating node {node.key}')
                raise
        # pprint(self.app)
        # import sys; sys.exit()

    RESERVED_SETTINGS = set(['id', 'process', 'scale', 'inbox', 'ifilters', 'ofilters', 'outbox'])

    def make_node(self, node):
        """Instantiate a node and all its upstream nodes, and wire them together."""
        if node.key not in self._node_backlog:
            return

        _l.debug(f'  node: {node.key}')
        _l.debug(f'  settings: {node.get("settings", dict())}')
        settings = node.get('settings', {})
        reserved_settings = self.RESERVED_SETTINGS.intersection(set(settings.keys()))
        if reserved_settings:
            plural = 's' if len(reserved_settings) > 1 else ''
            raise ConfigurationException(f'Settings for node {node.key} contains reserved '
                                         f'key{plural}: {", ".join(reserved_settings)}')

        outbox = dict()
        for channel, pipe in node.outbox.items():
            node.outbox[channel].instance = self.make_component(
                pipe.component, id=f'{node.key}.output.{channel}', **pipe.get('settings', {}))
            outbox[channel] = node.outbox[channel].instance

        inbox = dict()
        for channel, pipe in node.inbox.items():
            # _l.debug(f'  inbox.{channel}: {pipe}')
            if hasattr(pipe, 'instance'):
                # _l.debug(f'  * instance exists: {pipe.instance}')
                inbox[channel] = pipe.instance
                raise Exception('node instance exists')

            if isinstance(pipe, PipeRef):
                # _l.debug(f'  * connection {pipe}')
                node.inbox[channel] = pipe = Box(component=pipe, instance=pipe.resolve())
                # _l.debug(f'  * connected {pipe}')
            else:  # if 'component' in pipe:
                # _l.debug(f'  * component type: {type(pipe.component)}')
                pipe.instance = self.make_component(
                    pipe.component, id=f'{node.key}.input.{channel}', **pipe.get('settings', {}))
            inbox[channel] = pipe.instance

        ifilters = node.get('ifilters', {})
        # pprint(ifilters)
        for name, filter_ in ifilters.items():
            filter_.instance = self.make_component(
                resolve(filter_.component), id=f'{node.key}.filter.{name}',
                **filter_.get('settings', {}))
            # pprint([name, filter_])
        ifilters = PriorityRegistry(dict((k, f.instance) for k, f in ifilters.items()))
        ofilters = None
        node_args = dict(
            id=node.key, blocking=bool(node.get('blocking')), scale=node.get('scale'), inbox=inbox,
            ifilters=ifilters, ofilters=ofilters, outbox=outbox, **settings)
        if isclass(node.component) and issubclass(node.component, Node):
            node_class = node.component
        elif callable(node.component):
            node_class = Node
            node_args['process'] = node.component
        else:
            raise ConfigurationException(
                f'Node {node.key} should be a subclass of Node or a callable, '
                f'got {type(node.component)} instead')

        node.instance = self.make_component(node_class, **node_args)
        # print(f'    instance: {node.instance}')
        del self._node_backlog[node.key]

    def peer_node(self, spec, dependent):
        spec, channel, *_ = spec.rsplit(':', 1) + ['default']
        spec = spec.split('.')
        node = spec[-1]
        node_key = '.'.join(spec[:-1] + [node,])
        try:
            node = self.app.workflows[node_key]
        except KeyError:
            try:
                node = self.app.workflows[dependent.workflow][node_key]
            except KeyError:
                raise ConfigurationException(
                    f'Undefined node "{node_key}" (needed by {dependent.key})')
        return node, channel

    def make_component(self, class_, *args, **kwargs):
        return class_(self, *args, **kwargs)

    _SECRETS = set('account password secret'.split())

    def safe_settings(self, settings=__MISSING__):
        """Return modified settings where secrets have been hidden."""
        if settings is self.__MISSING__:
            settings = self.app
        if isdict(settings):
            settings = settings.copy()
            for key, value in settings.items():
                if isdict(value):
                    settings[key] = self.safe_settings(value)
                elif islist(value):
                    settings[key] = [self.safe_settings(i) for i in value]
                elif key in self._SECRETS:
                    settings[key] = '<secret>'
        return settings

    def run(self):
        """Create engine and run workflow."""
        self.engine = ETLEngine(self)
        self.engine.run()


def resolve(spec):
    """Parse component textual spec and import and return corresponding object."""
    try:
        module, attr, *_ = spec.rsplit(':', 1) + [None]
        # nameparts = module.split('.')
        # if nameparts[0] == 'pipekit':
        #     module = '.'.join(nameparts[1:])
        #     parent = 'pipekit'
        # else:
        #     parent = 'components'
        # module = import_module(f'{parent}.{module}')
        module = import_module(module)
        return getattr(module, attr)

    except Exception:
        raise ImportError(f'Failed to import component from spec: {spec}')


class ConfigurationException(Exception):
    pass
