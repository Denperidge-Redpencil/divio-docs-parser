from .Repo import Repo
from .DivioDocsEntry import _get_repo_docs
from .Section import sections
from .write_to_disk import clear_docs, generate_nav_if_needed
from typing import List
from .args import args_write_to_disk, args_repoconfigs

"""Entrypoint for the application"""

def main():
    """When this package is run directly, clear any existing docs and generate new ones based on args"""
    clear_docs()
    _get_docs_from_configured_repos()


def _get_docs_from_configured_repos():
    """Generate docs from configured repos"""
    for repoconfig in args_repoconfigs:
        get_docs_from_repo(repoconfig["url"])
    
    generate_nav_if_needed()


def get_docs_from_repo(git_url: str, write_to_disk=args_write_to_disk):
    repo = Repo(git_url)
    
    return _get_repo_docs(repo, write_to_disk=write_to_disk)


def get_docs_from_repos(git_urls: List[str]):
    for url in git_urls:
        get_docs_from_repo(url)
    generate_nav_if_needed()
    

if __name__ == "__main__":
    main()
