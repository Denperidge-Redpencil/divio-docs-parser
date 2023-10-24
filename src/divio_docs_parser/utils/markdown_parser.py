# Built-in imports
from os import getcwd
from os.path import exists, join, realpath, dirname, splitext
from typing import Dict, List
from base64 import b64encode

# Local imports
from .regex import grab_relative_hrefs
from ..Section import Section
"""
These functions are meant to wrap the Section class
to get & parse all sections from a file
"""


def _parse_sections_from_markdown_file(sections: List[Section], path: str, embed_relative_files=False) -> Dict[str, str]:
    """
    Wrapper for `_parse_sections_from_markdown_string`.
    Reads the file in the passed path and sends it to `_parse_sections_from_markdown_string`,
    setting the filename parameter to the passed path
    """
    with open(path, "r", encoding="UTF-8") as file:
        data = file.read()                

    return _parse_sections_from_markdown_string(sections, data, path, embed_relative_files)

def _import_relative_files(input_string, filename):
    # If filename is defined
    if filename is not None:
        path = dirname(filename)
    # Otherwise, use working directory
    else:
        path = dirname(getcwd())

    relative_files = grab_relative_hrefs(input_string)
    for relative_file in relative_files:
        file_path = realpath(join(path, relative_file["href"]))

        if not exists(file_path):
            continue

        ext = splitext(file_path)[1].lower().replace(".", "", 1)

        if ext == "":
            continue
        elif ext == "svg" or ext == "md":
            with open(file_path, "r", encoding="UTF-8") as file:
                file_contents = file.read()
            
            if ext == "svg":
                file_contents = file_contents.replace("\n", " ")
                file_contents = file_contents.replace("<svg", '\n\n<svg role="img"', 1)
                file_contents = file_contents.replace(">", f'><title>{relative_file["title"]}</title>', 1)
                file_contents = file_contents.replace("</svg>", "</svg>", 1)
            else:
                file_contents = f'<details>\n<summary>{relative_file["title"]}</summary>\n\n\n{file_contents}\n\n</details>'
        else:
            # Thanks to https://www.techcoil.com/blog/how-to-use-python-3-to-convert-your-images-to-base64-encoding/
            with open(file_path, "rb") as img:
                base64 = b64encode(img.read()).decode("utf-8")
            file_contents = f'<img alt="{relative_file["title"]}" src="data:image/{ext};base64,{base64}" />'

        input_string = input_string.replace(relative_file["tag"], f"\n\n\n{file_contents}\n\n\n")

    return input_string

def _parse_sections_from_markdown_string(sections: List[Section], input_string: str, filename=None, embed_relative_files=False) -> Dict[str, str]:
    """Parses a markdown string, returning a dict { `section_id`: `section_content` }"""
    extracted_sections = dict()

    # Relative file import
    if embed_relative_files:
        input_string = _import_relative_files(input_string, filename)

    for section in sections:
        section_in_content = section.header_in(input_string)
        if filename:
            section_in_filename =  section.header_in(filename, must_have_header_tags=False)
        else:
            section_in_filename = False

        found = section_in_content or section_in_filename

        if found:
            extracted_sections[section.id] = section.parse_from(input_string, import_whole_file=section_in_filename)
    
    return extracted_sections


def parse_sections_from_markdown(sections: List[Section], path_or_string: str, filename:str= None, embed_relative_files=False) -> Dict[str, str]:
    """
    Parses the passed markdown file or string. Returns { `section_id`: `content` }

    Params:
        `sections`: the sections to parse. You can define your own list, or use `DivioDocs._sectionObjects`

        `path_or_string`: path to a markdown file or a markdown string
        
        `filename`: filename is an optional parameter. It will only be used to check if the section regex matches it,
                    which causes the content of path_or_string to be added to that section. This will be automatically 
                    set to path if `path_or_string` is a path
                    
                    This is useful (for example) if your filename is ./documentation/tutorials/project.md
    """
    if exists(path_or_string):
        return _parse_sections_from_markdown_file(sections, path_or_string, embed_relative_files=embed_relative_files)
    else:
        return _parse_sections_from_markdown_string(sections, path_or_string, filename, embed_relative_files=embed_relative_files)
