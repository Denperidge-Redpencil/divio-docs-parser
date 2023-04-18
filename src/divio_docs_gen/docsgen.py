# Native imports
from os.path import exists, join
from os import makedirs
from shutil import rmtree
from pathlib import Path
from glob import glob
from typing import Union

# Local imports
from .sections import Section
from .args import args_docs_basedir
from .table import log_and_print, change_log_index

"""All code to help generate documentation"""

def filepath_in_exceptions(exceptioned_files: list, filepath: str):
    """Check if an alternative action has to be taken for a file"""
    try:
        log_and_print(f"Checking if {filepath} matches any of the following: {exceptioned_files}")
        return next(filter(lambda exceptioned_file: exceptioned_file.rsplit("/", 1)[0] in filepath, exceptioned_files))
    except StopIteration:
        return False  # the file is not part of the exception could not be found, return False
   

def clear_docs(sections: list):
    """Removes previously generated docs"""
    log_and_print("Clearing old docs...")
    change_log_index(1)

    sectionnames = [sections[section_id].name for section_id in sections]
    repodirs = glob(args_docs_basedir + "/*")

    log_and_print(f"section names to look for: {sectionnames}")
    log_and_print(f"names of directories to look in: {repodirs}")

    for repodir in repodirs:
        for sectionname in sectionnames:
            if exists(join(repodir, sectionname)):
                rmtree(repodir)
                log_and_print(f"{repodir}/{sectionname} exists, removed {repodir}")
                break
            else:
                log_and_print(f"{repodir}/{sectionname} does not exist, skipping")

    change_log_index(-1)
    log_and_print("... cleared old docs")

def markdown_link_from_filepath(name, link):
    """Helper to create a markdown link"""
    link = link.replace(" ", "%20")
    return f"- [{name}]({link})\n"

def join_and_make(path1, path2):
    """Join two paths, create the directory"""
    path = join(path1, path2)
    makedirs(path, exist_ok=True)
    return path

def make_and_get_repodir(reponame):
    """Create a directory for the repository in the docs basedir"""
    return join_and_make(args_docs_basedir, reponame)

def make_and_get_sectiondir(reponame, section: Union[str,Section]):
    """Create a directory for the section in the repository's folder"""
    if isinstance(section, Section):
        section = section.name
    
    return join_and_make(make_and_get_repodir(reponame), section)

def add_to_data_output(data_output: dict, reponame: str, section_name: str, content: str):
    if reponame not in data_output:
        data_output[reponame] = dict()

    if section_name not in data_output[reponame]:
        data_output[reponame][section_name] = content
    else:
        data_output[reponame][section_name] += content
    
    return data_output

def write_to_docs(reponame: str, section: Union[str,Section], content: str, filename="README.md", replaceContent=False, prepend=False) -> str:
    """Add CONTENT to the generated documentation. Optionally creates the needed directories, replaces contents..."""
    dir = make_and_get_sectiondir(reponame, section)
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
    return [ full_filename ]

def markdown_parent_nav():
    """Create a markdown link that navigates to the parent"""
    return markdown_link_from_filepath("../", "../")

def add_sibling_nav_to_files(filenames: list, include_parent_nav = True):
    """Iterative version of add_repo_nav_to_file"""
    for filename in filenames:
        add_sibling_nav_to_file(filename, include_parent_nav)

def add_sibling_nav_to_file(filename: str, include_parent_nav = True):
    """Add global navigation to the specified file"""
    # Save previous content
    with open(filename, "r", encoding="UTF-8") as file:
        prev_content = file.read()
    # Replace content
    with open(filename, "w", encoding="UTF-8") as file:
        # Whether to add ../
        if include_parent_nav:
            file.write(markdown_parent_nav())
        
        filepath = Path(filename)
        siblings = list(filepath.parent.glob("*"))
        for sibling in siblings:
            if sibling.name == filepath.name:
                continue
            file.write(markdown_link_from_filepath(sibling.name, sibling.name))
        
        file.write("\n")
            
        file.write(prev_content)


def generate_docs_nav_file(root: str, max_level: int, include_parent_nav = True, filename="README.md"):
    """Create a file purely for navigation"""
    path = args_docs_basedir + root
    files_to_link = glob(path + "/*" * max_level)
    with open(join(path, filename), "w", encoding="UTF-8") as file:
        if include_parent_nav:
            file.write(markdown_link_from_filepath("../", "../"))
        for file_to_link in files_to_link:
            file_to_link = file_to_link.replace(path, "").lstrip("/")
            file.write(markdown_link_from_filepath(file_to_link, file_to_link))
    

