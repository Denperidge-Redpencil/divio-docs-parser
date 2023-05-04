from os import makedirs
from os.path import exists, join


"""Generic helpers for write_to_docs"""

def _markdown_link_from_filepath(name, link):
    """Helper to create a markdown link"""
    link = link.replace(" ", "%20")
    return f"- [{name}]({link})\n"

def _join_paths_mkdir(path1, path2):
    """Join two paths, create the directory"""
    path = join(path1, path2)
    makedirs(path, exist_ok=True)
    return path




