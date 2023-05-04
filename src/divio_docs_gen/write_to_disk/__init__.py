# Native imports
from os.path import exists, join
from shutil import rmtree
from typing import Union, Dict

from ..args import args_docs_basedir
from .utils import _join_paths_mkdir


# Local imports
from ..Section import Section
from ..Repo import Repo
from ..args import args_docs_basedir
#from .table import log_and_print, change_log_index

from .utils import _join_paths_mkdir

"""Functions to assist in writing docs to disk"""


def clear_docs():
    """Removes previously generated docs"""
    if exists(args_docs_basedir):
        rmtree(args_docs_basedir)

def filepath_in_exceptions(exceptioned_files: list, filepath: str):
    """Check if an alternative action has to be taken for a file"""
    try:
        return next(filter(lambda exceptioned_file: exceptioned_file.rsplit("/", 1)[0] in filepath, exceptioned_files))
    except StopIteration:
        return False  # the file is not part of the exception could not be found, return False


def _make_and_get_repodir(repo_name):
    """Create a directory for the repository in the docs basedir"""
    return _join_paths_mkdir(args_docs_basedir, repo_name)
   
def _make_and_get_sectiondir(repo_name, section: Union[str,Section]):
    """Create a directory for the section in the repository's folder"""
    if isinstance(section, Section):
        section = section.name
    
    return _join_paths_mkdir(_make_and_get_repodir(repo_name), section)


def write_to_docs(repo_name: str, section: Union[str,Section], content: str, filename="README.md", replaceContent=False, prepend=False) -> str:
    """Add CONTENT to the generated documentation. Optionally creates the needed directories, replaces contents..."""
    dir = _make_and_get_sectiondir(repo_name, section)
    full_filename = join(dir, filename)
    mode = "a+" if (not replaceContent) and (not prepend) else "w"

    if prepend:
        with open(full_filename, "r", encoding="UTF-8") as file:
            original_data = file.read(content)

    with open(full_filename, mode, encoding="UTF-8") as file:
        file.write(content)
        if prepend:
            file.write(original_data)
    
    # Return without 
    return full_filename