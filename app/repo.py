from urllib import request, error
from json import loads

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
    print(url)
    print(data)
    return data


def get_repos(username: str) -> list:
    with request.urlopen(f"https://api.github.com/users/{username}/repos") as req:
        repos = loads(req.read())
    return repos


def get_repo_contents(username: str, reponame: str, path:str="", branch: str = ""):
    url = f"https://api.github.com/repos/{username}/{reponame}/contents/{path}" 
    if branch != "":
        url += f"?ref={branch}"

    try:
        with request.urlopen(url) as req:
            data = req.read().decode(req.headers.get_content_charset())  # https://stackoverflow.com/a/19156107
    except error.HTTPError as err:
        if err.code == 404:
            return ''
        else: 
            raise err
    return loads(data)

def get_markdown_from_repo_direcetory(username: str, reponame: str, path:str="", branch: str = ""):
    contents = get_repo_contents(username, reponame, path, branch)

    all_markdown = ""


    for file in contents:
        print(file['name'])
        print(file)
        if file["type"] == 'dir':
            print("dir")
            all_markdown += "\n" + get_markdown_from_repo_direcetory(username, reponame, file["path"], branch)
        elif file["name"].lower().endswith(".md"):
            print("Markdwon f")
            all_markdown += "\n" + get_file_contents(username, reponame, branch, file["path"])
    
    return all_markdown
        