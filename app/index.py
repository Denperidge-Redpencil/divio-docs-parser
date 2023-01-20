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

        readme_content = repo.filecontents("README.md")

        # Go over every section
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])
            
            markdown_files = repo.all_markdown_files
            found = False
            for filename in markdown_files:
                file_content = repo.filecontents(filename)
                section_in_content = repoSection.section.found_in(file_content, header=True)
                section_in_filename =  repoSection.section.found_in(filename)

                # If the file is a section file
                if section_in_filename:
                    found = True
                    repoSection.sourceContent = file_content
                    # Add the raw output
                    add_to_docs(repo.name, repoSection.section, file_content)
                # Else, if the section can be found in a general file
                elif section_in_content:
                    found = True
                    repoSection.sourceContent = file_content
                    # Add the output to docs, which is filtered
                    add_to_docs(repo.name, repoSection.section, repoSection.output)


            output = ok(padding=len(repoSection.section.headertext)) if found else nok(padding=len(repoSection.section.headertext))
        
        
            table = add_and_print(table, f" {output} |")
        print()

        



