from os import environ
from re import search

from dotenv import load_dotenv

from repo import get_repos, get_readme_contents
from colourstring import ok, nok
from sections import sections, RepoSection, Section
from table import setup_table, add_and_print

load_dotenv()


print("Checking repos for divio docs structure...")

headers = [
    "     repository     ", 
    sections['tutorials'].headertext, sections['howtos'].headertext,
    sections['explanations'].headertext, sections['references'].headertext]

table = setup_table(headers)



if __name__ == "__main__":
    username = environ.get('USERORORG')
    reponames = environ.get('REPOS').split(',')

    repos: list = [ repo for repo in get_repos(username) if repo['name'] in reponames ]

    for repo in repos:
        reponame = repo['name']
        main = repo['default_branch']

        # Start the row  with the repo name
        repoHeaderLength = len(headers[0])
        reponamePadded = reponame[:repoHeaderLength].center(repoHeaderLength)
        table = add_and_print(table, f"\n| {reponamePadded} |", f"Checking {reponame}...")

        readme_content = get_readme_contents(username, reponame, main)

        # Go over every section
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])
            
            # Check if its in the README
            section_in_readme = repoSection.section.found_in(readme_content)
            if section_in_readme:
                repoSection.sourceContent = readme_content
                print(repoSection.sectionContent)
            
            input()

            # TODO check if its in a file somewhere
            section_in_file = False


            

        


            output = ok(padding=len(repoSection.section.headertext)) if section_in_readme or section_in_file else nok(padding=len(repoSection.section.headertext))
        
        
            table = add_and_print(table, f" {output} |")
        print()

        



