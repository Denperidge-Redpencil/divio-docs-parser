# Built-in imports
from os.path import exists
from typing import Dict

# Local imports
from .Section import sections, Section

"""
These functions are meant to wrap the Section class
to get & parse all sections from a file
"""


def _parse_all_sections_from_markdown_file(path: str) -> Dict[str, str]:
    """Wrapper for _split_sections_from_markdown_string; reads the file in the passed path and sends it to _split_sections_from_markdown_string"""
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _parse_all_sections_from_markdown_string(data)

def _parse_all_sections_from_markdown_string(input_string: str, filename="") -> Dict[str, str]:
    """Parses a markdown string, returning a dict {section_id: section_content}"""
    extracted_sections = dict()

    for section_id in sections:
        section = sections[section_id]
        
        section_in_content = section.header_in(input_string, search_using_markdown_header=True)
        section_in_filename =  section.header_in(filename)

        found = section_in_content or section_in_filename

        if found:
            extracted_sections[section_id] = section.parse_from(input_string)
    
    return extracted_sections


def parse_all_sections_from_markdown(path_or_string: str) -> Dict[str, str]:
    """Parses the passed markdown file or string. Returns { section_id: content }"""
    if exists(path_or_string):
        return _parse_all_sections_from_markdown_file(path_or_string)
    else:
        return _parse_all_sections_from_markdown_string(path_or_string)
