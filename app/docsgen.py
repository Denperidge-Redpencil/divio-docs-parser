from os.path import exists, join
from os import makedirs, environ
from typing import Union
from shutil import rmtree
from glob import glob
from pathlib import Path

from dotenv import load_dotenv

from sections import Section
from nav import NavItem, markdown_link_from_filepath


load_dotenv()
docs_basedir = environ.get("DOCS", "docs/")
def clear_docs(sections: list):
    print(sections)
    sectionnames = [sections[section_id].name for section_id in sections]
    repodirs = glob(docs_basedir + "/*")

    for repodir in repodirs:
        for sectionname in sectionnames:
            if exists(join(repodir, sectionname)):
                rmtree(repodir)
                break

def join_and_make(path1, path2):
    path = join(path1, path2)
    makedirs(path, exist_ok=True)
    return path

def make_and_get_repodir(reponame):
    return join_and_make(docs_basedir, reponame)

def make_and_get_sectiondir(reponame, section: Union[str,Section]):
    if isinstance(section, Section):
        section = section.name
    
    return join_and_make(make_and_get_repodir(reponame), section)

def add_to_docs(reponame: str, section: Union[str,Section], content: str, filename="README.md", replaceContent=False, prepend=False) -> str:
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
    return full_filename

def markdown_parent_nav():
    return markdown_link_from_filepath("../", "../")

def add_repo_nav_to_files(filenames: list, include_parent_nav = True):
    for filename in filenames:
        add_repo_nav_to_file(filename, include_parent_nav)

def add_repo_nav_to_file(filename: str, include_parent_nav = True):
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
    path = docs_basedir + root
    files_to_link = glob(path + "/*" * max_level)
    with open(join(path, filename), "w", encoding="UTF-8") as file:
        if include_parent_nav:
            file.write(markdown_link_from_filepath("../", "../"))
        for file_to_link in files_to_link:
            file_to_link = file_to_link.replace(path, "").lstrip("/")
            file.write(markdown_link_from_filepath(file_to_link, file_to_link))
    

