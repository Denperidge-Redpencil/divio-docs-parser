from urllib import request, error
from json import loads

def get_readme_contents(username: str, reponame: str, branch: str) -> str:
    url = f"https://raw.githubusercontent.com/{username}/{reponame}/{branch}/README.md"
    try:
        with request.urlopen(url) as req:
            data = req.read().decode(req.headers.get_content_charset())  # https://stackoverflow.com/a/19156107
    except error.HTTPError as err:
        if err.code == 404:
            return ''
        else: 
            raise err
    return data

def get_repos(username: str) -> list:
    with request.urlopen(f"https://api.github.com/users/{username}/repos") as req:
        repos = loads(req.read())
    return repos