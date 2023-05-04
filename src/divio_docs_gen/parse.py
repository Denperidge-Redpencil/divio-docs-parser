
from .Section import sections, Section
from typing import Dict
from os.path import exists
from pathlib import Path
from .write_to_disk import write_to_docs
from .Repo import Repo

"""Parses """


class DivioDocsEntry():
    """An entry for a repo in the documentation. Contains the files for the section and their contents"""
    def __init__(self, repo) -> None:
        self.repo = repo
        self.sections = dict()
        for section_id in sections:
            self.sections[section_id] = dict()
    
    def add_to_section(self, section_id: str, filename="README.md", content: str=""):
        try:
            self.sections[section_id][filename] += content
        except KeyError:
            self.sections[section_id][filename] = content

    def get_section(self, section_id: str):
        return self.sections[section_id]
    
    def write_to_disk(self):
        for section_id in sections:
            section = self.get_section(section_id)
            
            for filename in section:

                write_to_docs(self.repo.name, section_id, content=section[filename], filename=filename)
        


def _parse_markdown_file(path: str):
    """(Private function) File-based wrapper for _parse_markdown_string"""
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _parse_markdown_string(data)

def _parse_markdown_string(input_string: str) -> Dict[str, str]:
    """(Private function) Parses a markdown string, returning a dict {section_id: section_content}"""
    content = dict()

    for section_id in sections:
        section = sections[section_id]
        
        section_in_content = section.found_in(input_string, header=True)


        if section_in_content:
            content[section_id] = section.extract_and_parse_section_from_string(input_string)

        # TODO implement copy & ignore
    
    return content


def markdown_to_sections_dict(path_or_string: str):
    """Parses a markdown file or string. Returns a dictionary of { section_id:  }"""
    if exists(path_or_string):
        parser = _parse_markdown_file
    else:
        parser = _parse_markdown_string
    
    return parser(path_or_string)


def repo_to_divio_docs_entries(repo: Repo, write_to_disk=False) -> DivioDocsEntry:
    """Parses all markdown files in a repo for all sections. Returns {section_name: {filename: content}}"""
    entry = DivioDocsEntry(repo)

    
    for file in repo.all_markdown_files:
        path = Path(file)

        parsed_file = markdown_to_sections_dict(path.absolute())
        for section_id in parsed_file:
            entry.add_to_section(section_id, path.name, parsed_file[section_id])
    
    #if write_to_disk:
     #   output_dict_to_docs(repo, output)

    """
    for section_id in sections:
        section = sections[section_id]
        # https://stackoverflow.com/a/16475444
        output[section.name] = output.pop(section_id)
    """ 
    
    return entry
