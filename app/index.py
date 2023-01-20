from os import environ
from re import search

from dotenv import load_dotenv

from repo import get_repos, get_file_contents, download_and_unzip, Repo
from colourstring import ok, nok
from sections import sections, RepoSection, Section
from table import setup_table, add_and_print
from docsgen import add_to_docs

load_dotenv()


print("Checking repos for divio docs structure...")

headers = [
    "     repository     ", 
    sections['tutorials'].headertext, sections['howtos'].headertext,
    sections['explanations'].headertext, sections['references'].headertext]

table = setup_table(headers)



if __name__ == "__main__":
    userOrOrgFallback = environ.get('USERORORG') or None  # Used as default repo owner
    reponames = environ.get('REPOS').split(',')

    repos: list = [ Repo(repo, owner=userOrOrgFallback) for repo in reponames ]

    for repo in repos:

        # Start the row  with the repo name
        repoHeaderLength = len(headers[0])
        reponamePadded = repo.name[:repoHeaderLength].center(repoHeaderLength)
        table = add_and_print(table, f"\n| {reponamePadded} |", f"Checking {repo.name}...")

        #readme_content = get_file_contents(username, reponame, main)

        # Go over every section
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])
            
            """
            # Check if its in the README
            section_in_readme = repoSection.section.found_in(readme_content)
            if section_in_readme:
                repoSection.sourceContent = readme_content
                add_to_docs(reponame, repoSection.section, repoSection.output)
            """

            # TODO check if its in a file somewhere
            section_in_file = False
            

            #print(get_markdown_from_repo_direcetory(username, reponame, "", main))


            input()


            

        


            output = ok(padding=len(repoSection.section.headertext)) if section_in_readme or section_in_file else nok(padding=len(repoSection.section.headertext))
        
        
            table = add_and_print(table, f" {output} |")
        print()

        



