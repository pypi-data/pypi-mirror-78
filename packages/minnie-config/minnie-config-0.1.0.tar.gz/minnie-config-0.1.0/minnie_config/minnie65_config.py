import datajoint as dj
import warnings
import json
import os
from pathlib import Path


segmentation_m65 = 2
segmentation_m65_str = '{:02d}'.format(segmentation_m65)

_schema_base_name = 'microns_minnie65_'
schema_name_m65 = _schema_base_name + segmentation_m65_str

path_obj = Path()

# External store paths + ensure the directories exist. For new segmentations create a subfolder.
if os.name == 'nt':
    path_obj = path_obj / r'\\at-storage.ad.bcm.edu\dj-stor01'
elif os.name == 'posix':
    path_obj = path_obj / '/mnt' / 'dj-stor01'
else:
    raise OSError('Unsupported OS pathing')

external_store_basepath = path_obj / 'platinum' / 'minnie65'
external_segmentation_path = path_obj / external_store_basepath / segmentation_m65_str
external_mesh_path = external_segmentation_path / 'meshes'
external_decimated_mesh_path = external_segmentation_path / 'decimated_meshes'
external_skeleton_path = external_segmentation_path / 'skeletons'

def verify_paths(create_if_missing=False):
    """
    This will verify if the paths exist.
    If the basepath does not exist however, it will not be created
    even if the "create_if_missing" argument is provided.
    """
    def warn_if_missing(path, warning_info, create_if_missing):
        warning_msg = 'Path to minnie65 folder does not exist at: {path}'
        if not path.exists():
            if create_if_missing:
                os.mkdir(path)
                return True
            else:
                msg = warning_msg.format(path=path)
                if warning_info:
                    msg += ' ({})'.format(warning_info)
                warnings.warn(msg)
                return False
        return True

    if warn_if_missing(external_store_basepath, 'dj-stor01 not mounted under /mnt ?', create_if_missing=False):
        warn_if_missing(external_segmentation_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_mesh_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_decimated_mesh_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_skeleton_path, '', create_if_missing=create_if_missing)
    else:
        raise OSError('dj-stor01 not available')

def set_configurations(host=None, cache_path=None): #, save_config=False # left out for because I'm not sure if having the stores be saved to config is a good idea or not
    # Set database host
    if host is not None:
        dj.config['database.host'] = str(host)

    # External filepath referrencing.
    stores_config = {
        'minnie65': {
            'protocol': 'file',
            'location': str(external_store_basepath),
            'stage': str(external_store_basepath)
        },
        'meshes': {
            'protocol': 'file',
            'location': str(external_mesh_path),
            'stage': str(external_mesh_path)
        },
        'decimated_meshes': {
            'protocol': 'file',
            'location': str(external_decimated_mesh_path),
            'stage': str(external_decimated_mesh_path)
        },
        'skeletons': {
            'protocol': 'file',
            'location': str(external_skeleton_path)
        }
    }

    if 'stores' not in dj.config:
        dj.config['stores'] = stores_config
    else:
        dj.config['stores'].update(stores_config)

    # External object cache
    if cache_path is not None:
        dj.config['cache'] = cache_path

    # Enable experimental datajoint features
    # These flags are required by 0.12.0+ (for now).
    dj.config['enable_python_native_blobs'] = True
    dj.errors._switch_filepath_types(True)
    dj.errors._switch_adapted_types(True)