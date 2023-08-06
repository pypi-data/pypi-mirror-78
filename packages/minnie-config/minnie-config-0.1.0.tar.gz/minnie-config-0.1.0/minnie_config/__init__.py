# Make sure the imports for the adapters and stuff can work correctly with how I have the configuration setup.

# Also enable this package to do some commandline mounting of dj-stor01 from at-storage03.ad.bcm.edu

from .minnie65_config import *
from .adapters import * # mesh, decimated_mesh, adapter_objects

# Just need to run verify_paths() and set_configurations()
# Or use this...

def configure_minnie(return_virtual_module=False, create_if_missing=False, host=None, cache_path=None):
    verify_paths(create_if_missing=create_if_missing)
    set_configurations(host=host, cache_path=cache_path)

    if return_virtual_module:
        import datajoint as dj
        return dj.create_virtual_module('minnie', schema_name_m65, add_objects=adapter_objects)