
from .Section import sections, Section
from typing import Dict
from os.path import exists
from pathlib import Path
from .write_to_disk import write_to_docs
from .Repo import Repo
from .args import args_write_to_disk

"""Everything concerning creating DivioDocsEntry objects: extracting sections from the Repo's markdown files"""

class DivioDocsEntry():
    """This represents a divio docs entry: all the docs for a repo, correctly structured. Contains section, filenames and their contents"""
    def __init__(self, repo: Repo) -> None:
        self.repo = repo
        self.repo_sections = dict()
        for section_id in sections:
            self.repo_sections[section_id] = dict()
    
    def add_to_repo_section(self, section_id: str, filename="README.md", content: str=""):
        try:
            self.repo_sections[section_id][filename] += content
        except KeyError:
            self.repo_sections[section_id][filename] = content

    def get_repo_section(self, section_id: str):
        return self.repo_sections[section_id]
    
    def write_to_disk(self):
        for section_id in self.repo_sections:
            print(section_id)
            section = self.get_repo_section(section_id)

            print(section)

            
            for filename in section:
                write_to_docs(self.repo.name, section_id, content=section[filename], filename=filename)
    
    def import_from_markdown(self, path_or_string: str, filename="README.md"):
        parsed_file = _split_sections_from_markdown(path_or_string)
        for section_id in parsed_file:
            self.add_to_repo_section(section_id, filename, parsed_file[section_id])
    
    

def _split_sections_from_markdown_file(path: str) -> Dict[str, str]:
    """(Private function) File-based wrapper for _split_sections_from_markdown_string"""
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _split_sections_from_markdown_string(data)

def _split_sections_from_markdown_string(input_string: str, filename="") -> Dict[str, str]:
    """(Private function) Parses a markdown string, returning a dict {section_id: section_content}"""
    markdown_sections = dict()


    for section_id in sections:
        section = sections[section_id]
        
        section_in_content = section.found_in(input_string, header=True)
        section_in_filename =  section.found_in(filename)

        found = section_in_content or section_in_filename


        if found:
            markdown_sections[section_id] = section.extract_and_parse_section_from_string(input_string)

        # TODO implement copy & ignore
    
    return markdown_sections


def _split_sections_from_markdown(path_or_string: str):
    """Parses a markdown file or string. Returns a dictionary of { section_id: content }"""
    if exists(path_or_string):
        return _split_sections_from_markdown_file(path_or_string)
    else:
        return _split_sections_from_markdown_string(path_or_string)


def _get_repo_docs(repo: Repo, write_to_disk=False) -> DivioDocsEntry:
    """Parses all markdown files in a repo for all sections. Returns a DivioDocsEntry object"""
    entry = DivioDocsEntry(repo)

    for file in repo.all_markdown_files:
        path = Path(file)
        entry.import_from_markdown(path.absolute(), path.name)
    
    if write_to_disk:
        entry.write_to_disk()


    return entry
