from os import environ

from repo import get_repos, get_readme_contents
from colourstring import ok, nok
from sections import sections
from dotenv import load_dotenv
load_dotenv()


print("Checking repos for divio docs structure...")

headers = [
    "     repository     ", 
    sections['tutorials'].headertext, sections['howtos'].headertext,
    sections['explanations'].headertext, sections['references'].headertext]

# Table generation
print("|", end="")
for header in headers:
    print(f" {header} ", end="|")
print("\n|", end="")
for header in headers:
    print(f" {'-' * len(header)} ", end="|")
print()


if __name__ == "__main__":
    username = environ.get('USERORORG')
    reponames = environ.get('REPOS').split(',')

    repos: list = [ repo for repo in get_repos(username) if repo['name'] in reponames ]

    for repo in repos:
        reponame = repo['name']
        main = repo['default_branch']

        content = get_readme_contents(username, reponame, main)

        repoHeaderLength = len(headers[0])
        reponamePadded = reponame[:repoHeaderLength].center(repoHeaderLength)

        print(f"| {reponamePadded} ", end="|")

        for i, section_id in enumerate(sections):
            section = sections[section_id]

            length = len(headers[i+1])  # The first header is already handled
            
            result = ok(padding=length) if section.found_in(content) else nok(padding=length)


            print(f" {result} ", end="|")
        print()

        



