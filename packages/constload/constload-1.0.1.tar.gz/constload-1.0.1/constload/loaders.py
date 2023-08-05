import json as _json

_yaml_avail = True
try:
    import yaml
except ImportError:
    _yaml_avail = False

if _yaml_avail:
    try:
        from yaml import CLoader as yaml_loader
    except ImportError:
        from yaml import Loader as yaml_loader


class Loaders:
    @classmethod
    def json(_, data):
        return _json.loads(data)

    @classmethod
    def yaml_safe(_, data):
        if _yaml_avail:
            return yaml.safe_load(data)
        else:
            raise RuntimeError("PyYAML is not installed. Install it with either 'pip install constload[yaml]' or "
                               "'pip install PyYAML'")

    @classmethod
    def yaml_unsafe(_, data):
        if _yaml_avail:
            return yaml.load(data, Loader=yaml_loader)
        else:
            raise RuntimeError("PyYAML is not installed. Install it with either 'pip install constload[yaml]' or "
                               "'pip install PyYAML'")
