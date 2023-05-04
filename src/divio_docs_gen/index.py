# Native imports
from typing import List
# Local imports
from .Repo import Repo
from .DivioDocsEntry import _get_repo_docs
from .write_to_disk import clear_docs, generate_nav_as_needed
from .args import args_write_to_disk, args_repoconfigs

"""Entrypoint for the application"""

def main():
    """When this package is run directly, clear any existing docs and generate new ones based on args"""
    clear_docs()
    _docs_from_configured_repos()


def _docs_from_configured_repos():
    """Generate docs from configured repos"""
    for repoconfig in args_repoconfigs:
        docs_from_repo(repoconfig["url"])
    
    generate_nav_as_needed()


def docs_from_repo(git_url: str, write_to_disk=args_write_to_disk):
    """Generate documentation from the passed git url. This function does NOT automatically create nav files; make sure to run generate_nav_if_needed if desired"""
    repo = Repo(git_url)
    return _get_repo_docs(repo, write_to_disk=write_to_disk)


def docs_from_repos(git_urls: List[str]):
    """Generate documentation from passed git urls. This function DOES automatically create nav files, if enabled in docs.conf or the passed args"""
    for url in git_urls:
        docs_from_repo(url)
    generate_nav_as_needed()
    

if __name__ == "__main__":
    main()
