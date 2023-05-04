
from pathlib import Path
from ..args import args_docs_basedir
from glob import glob
from os.path import join
from .utils import _markdown_link_from_filepath




def _markdown_link_to_parent():
    """Create a markdown link that navigates to the parent"""
    return _markdown_link_from_filepath("../", "../")

def add_nav_header_to_file(filename: str, include_parent_nav = True):
    """Add global navigation to the specified file"""
    # Save previous content
    with open(filename, "r", encoding="UTF-8") as file:
        prev_content = file.read()
    # Replace content
    with open(filename, "w", encoding="UTF-8") as file:
        # Whether to add a navigation to the parent dir
        if include_parent_nav:
            file.write(_markdown_link_to_parent())

        filepath = Path(filename)
        siblings = list(filepath.parent.glob("*"))
        for sibling in siblings:
            if sibling.name == filepath.name:
                continue
            file.write(_markdown_link_from_filepath(sibling.name, sibling.name))

        file.write("\n")
        file.write(prev_content)


def add_nav_header_to_files(filenames: list, include_parent_nav = True):
    """Iterative version of add_repo_nav_to_file"""
    for filename in filenames:
        add_nav_header_to_file(filename, include_parent_nav)

def add_nav_header_to_all_docs(include_parent_nav = True):
    doc_files = glob(args_docs_basedir + "/**/*.md", recursive=True)
    add_nav_header_to_files(doc_files)

def generate_docs_nav_file(subdirectory: str, max_level: int, include_parent_nav = True, filename="README.md"):
    """Create a file purely for navigation"""
    base_path = args_docs_basedir + subdirectory
    files_to_link = glob(base_path + "/*" * max_level)
    with open(join(base_path, filename), "w", encoding="UTF-8") as file:
        if include_parent_nav:
            file.write(_markdown_link_from_filepath("../", "../"))
        for file_to_link in files_to_link:
            file_to_link = file_to_link.replace(base_path, "").lstrip("/")
            file.write(_markdown_link_from_filepath(file_to_link, file_to_link))

def create_top_level_nav():
    generate_docs_nav_file("", 1, include_parent_nav=False)
