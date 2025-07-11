from pathlib import Path

def get_project_root(marker_file='README.md'):
    """ Returns the root directory of the project (in case of running in other dirs) 
    by walking up the directory tree and looking for the README.md' file
    """
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / marker_file).exists():
            return parent
    raise FileNotFoundError(f'Could not find project root with marker {marker_file} from {current}')

def get_data_raw_path():
    """ Returns the path to the raw data directory """
    return get_project_root() / 'data' / 'raw'

def get_data_processed_path():
    """ Returns the path to the processed data directory """
    return get_project_root() / 'data' / 'processed'