# Native imports
from glob import glob
from os import mkdir
from os.path import join, exists
from shutil import rmtree
from urllib import request, error
from json import loads
from zipfile import ZipFile
# Local imports
from table import log_and_print

"""Repo class, including utilities to download Repository files"""

tmp_dir = "tmp/"
if exists(tmp_dir):
    rmtree(tmp_dir)
mkdir(tmp_dir)

class Repo():
    def __init__(self, repos_data: list, path:str=None, owner:str=None, reponame:str=None, branch:str=None, config: dict=None) -> None:
        """Constructors a Repo class instance, applies configuration and downloads files"""

        self.files_to_copy = []
        self.files_to_ignore = []
        print(config)
        if config:
            path = config["path"]
            if not owner:
                owner = config["fallbackowner"]

            if "copy" in config:
                self.files_to_copy = config["copy"].split(",")
            if "ignore" in config:
                self.files_to_ignore = config["ignore"].split(",")

        # If the path is provided
        if path:
            # And contains the branch, remove it and set the branch variable to handle later
            if "@" in path:
                splitPath = path.split("@")
                branch = splitPath[1]
                path = splitPath[0]
            

            # Owner specified in path
            if "/" in path:
                # Extract the path info into userOrOrg & reponame
                owner, reponame = path.split("/")
            # If the owner hasn't been specified in the path, but a fallback is given
            elif owner:
                # then the provided path is the reponame
                reponame = path
            # If no owner has been specified at all, raise ValueError
            else:
                raise ValueError(f"{path} is missing the user/org name and/or the repo name!")

                

        if owner and reponame:
            self.owner = owner
            self.name = reponame
            
        else:
            raise ValueError("The repo path or (userOrOrg and repoName) have to be defined!")

        # If the path has either been explicitly defined or extracted from path
        if branch:
            self.branch = branch
        else:
            print(repos_data)
            print(self.name)
            self.branch = next(filter(lambda repo_data: repo_data['name'].lower() == self.name.lower(), repos_data))['default_branch']
        
        download_and_unzip(self.zip_url, self.tmp_files)


    @property
    def path(self) -> str:
        """Returns REPO_OWNER/REPO_NAME"""
        return self.owner + "/" + self.name

    @property
    def zip_url(self) -> str:
        """Returns an URL to download the repo files"""
        return f"https://github.com/{self.path}/archive/refs/heads/{self.branch}.zip"
    
    @property
    def tmp_files(self) -> str:
        """Returns path to temporarily downloaded files"""
        # Follows GitHub zip file naming
        return f"{tmp_dir}/{self.name}-{self.branch}"
    
    def filepath(self, path) -> str:
        """Returns the path to a file, automatically adding the path to the tmp files if needed"""
        if path.startswith(self.tmp_files):
            return path
        return join(self.tmp_files, path)

    def glob(self, path):
        """Run a glob on the specified path within this repo"""
        return glob(self.filepath(path), recursive=True)

    @property
    def all_markdown_files(self):
        """Returns a list of all markdown files of the repo"""
        return self.glob("**/*.md")

    def filecontents(self, path):
        """Reads contents from specified file"""
        # If a relative path is given, append
        path = self.filepath(path)

        try:
            with open(path, "r", encoding="UTF-8") as file:
                data = file.read()
        except FileNotFoundError:
            data = ""
            
        return data
    
    


def download_and_unzip(url, dest):
    """Helper function to download URL & unzip it to DEST"""
    filename, res = request.urlretrieve(url, dest + ".zip")
    ZipFile(filename).extractall(tmp_dir)
    #ZipFile()
    #with request.urlopen(url) as req:
     #   ZipFile(StringIO() req.read()).extractall(dest)


def get_file_contents(username: str, reponame: str, branch: str, path: str="README.md") -> str:
    """Get file contents directly from a specific repository's assets host"""
    url = f"https://raw.githubusercontent.com/{username}/{reponame}/{branch}/{path}"
    try:
        with request.urlopen(url) as req:
            data = req.read().decode(req.headers.get_content_charset())  # https://stackoverflow.com/a/19156107
    except error.HTTPError as err:
        if err.code == 404:
            return ''
        else: 
            raise err
    return data


def get_json(url: str):
    """Request json from URL"""
    log_and_print(f"Fetching JSON from {url}...")
    with request.urlopen(url) as req:
        data = loads(req.read())
    log_and_print(f"...fetched JSON")
    
    return data

def get_repos(owner: str) -> list:
    """Get list of repos from specified owner"""
    url = f"https://api.github.com/users/{owner}/repos"
    return get_json(url)

# Unused due to too many requests
def get_repo_data(ownerAndReponame: str):
    """Get data from a singular repo"""
    url = f"https://api.github.com/repos/{ownerAndReponame}"
    return get_json(url)

