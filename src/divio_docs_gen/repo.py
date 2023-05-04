# Native imports
from glob import glob
from os import mkdir, system, makedirs
from os.path import join, exists
from shutil import rmtree
from urllib import request, error
from json import loads
from zipfile import ZipFile
# Local imports
from .logging.table import log_and_print
from git.repo import Repo as GitRepo
from slugify import slugify
from .parse import markdown_to_sections_dict

"""Repo class, including utilities to download Repository files"""

repos_dir = "repos/"
makedirs(repos_dir, exist_ok=True)

class Repo():
    def __init__(self, url: str) -> None:
        """Constructors a Repo class instance, applies configuration and downloads files"""
        #self.files_to_copy = []
        #self.files_to_ignore = []
        self.url = url

        if not self.exists_locally:
            self.gitpython = GitRepo.clone_from(url, self.local_dir)
        else:
            self.gitpython = GitRepo(self.local_dir)
            self.gitpython.remotes[0].pull()
        

    @property
    def exists_locally(self) -> bool:
        return exists(self.local_dir)

    @property
    def slug(self) -> str:
        return slugify(self.url)

    @property
    def local_dir(self) -> str:
        """Returns path to temporarily downloaded files"""
        # Follows GitHub zip file naming
        return f"{repos_dir}/{self.slug}"
    
    def get_file(self, path) -> str:
        """Returns the path to a file, automatically prefixing the tmp_files path if needed"""
        if path.startswith(self.local_dir):
            return path
        return join(self.local_dir, path)

    def find_files(self, path):
        """Run a glob on the specified path within this repo"""
        return glob(self.get_file(path), recursive=True)

    @property
    def all_markdown_files(self):
        """Returns a list of all markdown files of the repo"""
        return self.find_files("**/*.md")

    def get_file_contents(self, path):
        """Reads contents from specified file"""
        # If a relative path is given, append
        path = self.get_file(path)

        try:
            with open(path, "r", encoding="UTF-8") as file:
                data = file.read()
        except FileNotFoundError:
            raise FileNotFoundError

        return data
    

