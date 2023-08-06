import logging
import os


__all__ = 'Tree', 'flatten'

logger = logging.getLogger(__package__)


class AttrDict(dict):
    """
    Attribute key access dictionary.

    It is used for ``jsonpyth`` filter expressions which operate over
    dictionaries and would need subscription otherwise.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class Tree:

    _procfile_registry = None

    _skip_self = None
    _dictcls = None

    def __init__(self, proc_file_registry, skip_self=True, dictcls=AttrDict):
        self._procfile_registry = proc_file_registry
        self._skip_self = skip_self
        self._dictcls = dictcls

    @staticmethod
    def get_pid_list():
        return [int(p) for p in os.listdir('/proc') if p.isdigit()]

    def _read_process_dict(self, pid):
        result = self._dictcls()
        for name, fn in self._procfile_registry.items():
            try:
                with open(f'/proc/{pid}/{name}', 'rb') as f:
                    result[name] = fn(f.read(), dictcls=self._dictcls)
            except PermissionError as ex:
                logger.warning(str(ex))
                result[name] = self._dictcls(fn.empty) if isinstance(fn.empty, dict) else fn.empty
        return result

    def get_nodemap(self):
        if 'stat' not in self._procfile_registry:
            raise RuntimeError('stat file reader is required')

        pids = self.get_pid_list()
        if self._skip_self:
            pids.remove(os.getpid())

        lookup = {}
        for p in list(pids):
            try:
                lookup[p] = self._read_process_dict(p)
            except FileNotFoundError:
                # Race condition
                pids.remove(p)

        for p in pids:
            node = lookup[p]
            if node['stat']['ppid'] != 0:
                lookup[node['stat']['ppid']].setdefault('children', []).append(node)

        return lookup

    def get_root(self):
        return self.get_nodemap()[1]


def _flatten_hierarchy(node_list):
    """Turn tree node list recursively into a flat list."""

    result = []
    for node in node_list:
        result.append(node)
        result.extend(_flatten_hierarchy(getattr(node, 'children', [])))

    return result

def _flatten_file_keys(node: dict, procfile_list):
    """Make flat dictionary out of proc file nested dictionary."""

    result = {}
    for procfile_name, value in node.items():
        if procfile_name not in procfile_list:
            continue

        if isinstance(value, dict):
            result.update({f'{procfile_name}_{k}': v for k, v in value.items()})
        else:
            result[procfile_name] = value

    return result

def flatten(data, procfile_list):
    """
    Make a PID → flat mapping out of a subtree or node list.

    Only keys occurring in ``procfile_list`` are taken into result.
    """

    result = _flatten_hierarchy(data if isinstance(data, list) else [data])
    result = {n['stat']['pid']: _flatten_file_keys(n, procfile_list) for n in result}
    return list(result.values())
