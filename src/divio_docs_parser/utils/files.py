# Built-in imports
from os.path import join, abspath, isfile
from glob import glob

"""Utilities for finding files"""

def list_all_files(path: str, selector="*"):
    """
    List the absolute paths of every file in `path` that matches the provided glob `selector`.
    
    If no selector is provided, every files will be matched
    """
    path = abspath(path)
    files = glob(join(path, "**/" + selector), recursive=True)
    return [file for file in files if isfile(file)]

def list_all_markdown_files(path: str):
    """
    List the absolute paths of every markdown file in the given `path`.

    Wraps the list_all_files function
    """
    return list_all_files(path, "*.md")

