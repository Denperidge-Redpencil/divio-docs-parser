# Native imports
from glob import glob
from os import makedirs
from os.path import join, exists
# Local imports
from git.repo import Repo as GitRepo
from slugify import slugify

"""Repo class: utilities to clone/pull the repoand access the files"""

repos_dir = "repos/"
makedirs(repos_dir, exist_ok=True)

class Repo():
    def __init__(self, url: str) -> None:
        """Constructs a Repo class instance, applies configuration (TODO) and clones/pulls the repo"""
        #self.files_to_copy = []
        #self.files_to_ignore = []
        self.url = url

        if not self.exists_locally:
            self.gitpython = GitRepo.clone_from(url, self.local_dir)
        else:
            self.gitpython = GitRepo(self.local_dir)
            self.gitpython.remotes[0].pull()

        
    @property
    def name(self) -> str:
        return self.url.rsplit("/", maxsplit=1)[1].rsplit(".", maxsplit=1)[0]

    @property
    def exists_locally(self) -> bool:
        return exists(self.local_dir)

    @property
    def slug(self) -> str:
        return slugify(self.url)

    @property
    def local_dir(self) -> str:
        """Returns path to local files for the repo"""
        # Follows GitHub zip file naming
        return f"{repos_dir}/{self.slug}"
    
    def get_file(self, path) -> str:
        """Returns the path to a file, automatically prefixing the repos dir path if needed"""
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
    

