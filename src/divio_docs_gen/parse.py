
from .sections import sections
from typing import List, Dict
from os.path import exists
from pathlib import Path


def markdown_to_sections_dict(path_or_string: str):
    """Parses a markdown file or string. Returns a dictionary of { section_id:  }"""
    if exists(path_or_string):
        parser = _parse_markdown_file
    else:
        parser = _parse_markdown_string
    
    return parser(path_or_string)

def _parse_markdown_file(path: str):
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _parse_markdown_string(data)

def _parse_markdown_string(input_string: str) -> Dict[str, str]:
    """Parses a markdown string, returning a dict {section_id: section_content}"""
    content = dict()

    for i, section_id in enumerate(sections):
        section = sections[section_id]
        section_in_content = section.found_in(input_string, header=True)

        print(section.name + " ### " + str(section_in_content))

        if section_in_content:
            content[section_id] = section.extract_and_parse_section_from_string(input_string)

        # TODO implement copy & ignore
    
    return content




def parse_docs(repo):
    """Parses all markdown files in a repo for all sections. Returns {section_id: {filename: content}}"""
    output = {}
    for section_id in sections:
        output[section_id] = dict()

    for file in repo.all_markdown_files:
        path = Path(file)

        parsed_file = markdown_to_sections_dict(path.absolute())
        for section_id in parsed_file:
            output[section_id][path.name] = parsed_file[section_id]

    return output
