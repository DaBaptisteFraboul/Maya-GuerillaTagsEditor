import os


def get_abspath(relative_path:str) -> str:
    """
    Get a clean absolute path given the relative path to the script
    :param relative_path:
    :return:
    """
    path_base = os.path.dirname(__file__)
    path = os.path.join(path_base, relative_path)
    path = path.replace('\\','/')
    return path
