# Built-in imports
from os.path import exists
from typing import Dict

# Local imports
from .Section import sections




def _split_sections_from_markdown_file(path: str) -> DivioDocs:
    """Wrapper for _split_sections_from_markdown_string; reads the file in the passed path and sends it to _split_sections_from_markdown_string"""
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()
    return _split_sections_from_markdown_string(data)

def _split_sections_from_markdown_string(input_string: str, filename="") -> DivioDocs:
    """Parses a markdown string, returning a dict {section_id: section_content}"""
    markdown_sections = DivioDocs()


    for section_id in sections:
        section = sections[section_id]
        
        section_in_content = section.found_in(input_string, search_using_markdown_header=True)
        section_in_filename =  section.found_in(filename)

        found = section_in_content or section_in_filename


        if found:
            markdown_sections.set(section_id, section.extract_and_parse_section_from_string(input_string))
    
    return markdown_sections


def split_sections_from_markdown(path_or_string: str) -> DivioDocs:
    """Parses the passed markdown file or string. Returns { section_id: content }"""
    if exists(path_or_string):
        return _split_sections_from_markdown_file(path_or_string)
    else:
        return _split_sections_from_markdown_string(path_or_string)
