from .Repo import Repo
from .DivioDocsEntry import _get_repo_docs
from .Section import sections
from .write_to_disk import clear_docs
from .write_to_disk.nav import create_top_level_nav,add_nav_header_to_all_docs,  add_nav_header_to_file
from typing import List
from .args import args_write_to_disk, args_generate_nav

"""Entrypoint for the application"""

def main():
    clear_docs()
    
    get_docs_from_repos([
        "https://github.com/mu-semtech/mu-cl-resources", 
        "https://github.com/denperidge-redpencil/project"])
    


def get_docs_from_repo(git_url: str, write_to_disk=args_write_to_disk):
    repo = Repo(git_url)
    
    return _get_repo_docs(repo, write_to_disk=write_to_disk)


def get_docs_from_repos(git_urls: List[str]):
    for url in git_urls:
        get_docs_from_repo(url)
    
    add_nav_header_to_all_docs()
    create_top_level_nav()

if __name__ == "__main__":
    main()
