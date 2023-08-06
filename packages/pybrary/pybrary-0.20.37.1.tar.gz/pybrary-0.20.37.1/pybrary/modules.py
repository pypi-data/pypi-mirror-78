from importlib.util import spec_from_file_location
from importlib.util import module_from_spec


def load(mod_name, mod_file):
    spec = spec_from_file_location(mod_name, mod_file)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
