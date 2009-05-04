"""File utilities."""
import os

def create_dir_if_not_exist(dir_path):
    """Like os.makedirs() but create the directory if it does not exist."""
    if not os.access(dir_path, os.F_OK):
        os.makedirs(dir_path)
        
def create_file_if_not_exist(file_path, default_content=''):
    """
    Test for file existence. If it does not exist create a new file with
    the given text content.
    """
    if not os.access(file_path, os.F_OK):
        f = open(file_path, 'w')
        f.write(default_content)
        f.close()
