from os.path import exists, join
from os import makedirs
from typing import Union

from sections import Section

docs_basedir = "docs/"

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

def add_to_docs(reponame: str, section: Union[str,Section], content: str, filename="README.md", replaceContent=False):
    dir = make_and_get_sectiondir(reponame, section)
    mode = "a+" if not replaceContent else "w"

    with open(join(dir, filename), mode, encoding="UTF-8") as file:
        file.write(content)
