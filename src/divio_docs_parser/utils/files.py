# Built-in imports
from os.path import join, abspath, isfile
from glob import glob

"""Utilities for finding files"""

def list_all_files(path: str, selector="*"):
    """(Method) Run a glob on the specified path within the provided path"""
    path = abspath(path)
    files = glob(join(path, "**/" + selector), recursive=True)
    return [file for file in files if isfile(file)]

def list_all_markdown_files(path):
    """(Property) Returns a list of all markdown files of the repo"""
    return list_all_files(path, "*.md")

