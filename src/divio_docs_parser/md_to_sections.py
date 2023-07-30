# Built-in imports
from os.path import exists
from typing import Dict, List

# Local imports
from .Section import Section
"""
These functions are meant to wrap the Section class
to get & parse all sections from a file
"""


def _parse_sections_from_markdown_file(sections: List[Section], path: str) -> Dict[str, str]:
    """Wrapper for _split_sections_from_markdown_string; reads the file in the passed path and sends it to _split_sections_from_markdown_string"""
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _parse_sections_from_markdown_string(sections, data, path)

def _parse_sections_from_markdown_string(sections: List[Section], input_string: str, filename=None) -> Dict[str, str]:
    """Parses a markdown string, returning a dict {section_id: section_content}"""
    extracted_sections = dict()

    for section in sections:
        section_in_content = section.header_in(input_string)
        if filename:
            section_in_filename =  section.header_in(filename, must_have_header_tags=False)
        else:
            section_in_filename = False

        found = section_in_content or section_in_filename

        if found:
            extracted_sections[section.name] = section.parse_from(input_string)
    
    return extracted_sections


def parse_sections_from_markdown(sections: List[Section], path_or_string: str, filename:str= None) -> Dict[str, str]:
    """Parses the passed markdown file or string. Returns { section_id: content }"""
    if exists(path_or_string):
        return _parse_sections_from_markdown_file(sections, path_or_string)
    else:
        return _parse_sections_from_markdown_string(sections, path_or_string, filename)
