from urllib import request, error
from json import loads
from os import mkdir
from os.path import join, exists
from shutil import rmtree
from zipfile import ZipFile

tmp_dir = "tmp/"
if exists(tmp_dir):
    rmtree(tmp_dir)
mkdir(tmp_dir)

class Repo():
    def __init__(self, path:str=None, owner:str=None, reponame:str=None, branch:str=None) -> None:
        # If the path is provided
        if path:
            # And contains the branch, remove it and set the branch variable to handle later
            if "@" in path:
                splitPath = path.split("@")
                branch = splitPath[1]
                path = splitPath[0]
            
            # Extract the path info into userOrOrg & reponame
            print(path)
            
            try:
                owner, reponame = path.split("/")
            except ValueError:
                raise ValueError(f"{path} is missing the user/org name, or the repo name!")

        if owner and reponame:
            self.owner = owner
            self.name = reponame
            
        else:
            raise ValueError("The repo path or (userOrOrg and repoName) have to be defined!")

        # If the path has either been explicitly defined or extracted from path
        if branch:
            self.branch = branch
        else:
            self.branch = get_repo_data(self.path)['default_branch']
        
        download_and_unzip(self.zip_url, self.tmp_files)


    @property
    def path(self):
        return self.owner + "/" + self.name

    @property
    def zip_url(self):
        return f"https://github.com/{self.path}/archive/refs/heads/{self.branch}.zip"
    
    @property
    def tmp_files(self):
        # Follows GitHub zip file naming
        return f"{tmp_dir}/{self.name}-{self.branch}"
    
    


def download_and_unzip(url, dest):
    filename, res = request.urlretrieve(url, dest + ".zip")
    ZipFile(filename).extractall(tmp_dir)
    #ZipFile()
    #with request.urlopen(url) as req:
     #   ZipFile(StringIO() req.read()).extractall(dest)


def get_file_contents(username: str, reponame: str, branch: str, path: str="README.md") -> str:
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


def get_repos(userOrOrg: str) -> list:
    with request.urlopen(f"https://api.github.com/users/{userOrOrg}/repos") as req:
        repos = loads(req.read())
    return repos


def get_repo_data(userAndReponame: str):
    with request.urlopen(f"https://api.github.com/repos/{userAndReponame}") as req:
        repo = loads(req.read())
    return repo

