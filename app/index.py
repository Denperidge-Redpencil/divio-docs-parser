from os import environ
from re import search

from dotenv import load_dotenv

from repo import get_repos, get_file_contents, download_and_unzip, Repo
from colourstring import ok, nok
from sections import sections, RepoSection, Section
from table import setup_table, add_and_print, print_table
from docsgen import add_to_docs, add_repo_nav_to_files, generate_docs_nav_file

load_dotenv()



headers = [
    "     repository     ", 
    sections['tutorials'].headertext, sections['howtos'].headertext,
    sections['explanations'].headertext, sections['references'].headertext]

table = setup_table(headers)

print_table(table, "Checking repos for divio docs structure...")

nav = bool(environ.get("NAV"))
if nav:
    print_table(table, "Adding navigation headers to the files...")
    

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

        created_files = []

        # Go over every section
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])
            
            markdown_files = repo.all_markdown_files
            found = False
            for filename in markdown_files:
                file_content = repo.filecontents(filename)
                section_in_content = repoSection.section.found_in(file_content, header=True)
                section_in_filename =  repoSection.section.found_in(filename)

                # Written longer than needed for clarity
                found = True if section_in_content or section_in_filename else False

                print_msg = f"Adding {repo.name} - {repoSection.section.name} from "
                # If the file is a section file
                if section_in_filename:
                    print_msg += "filename"
                    print_table(table, print_msg)
                    repoSection.sourceContent = file_content
                    # Add the raw output
                    created_files.append(add_to_docs(repo.name, repoSection.section, file_content))
                    print_table(table, print_msg.replace("Adding", "Added"))
                # Else, if the section can be found in a general file
                elif section_in_content:
                    print_msg += "filecontent"
                    print_table(table, print_msg)
                    repoSection.sourceContent = file_content
                    # Add the output to docs, which is filtered
                    created_files.append(add_to_docs(repo.name, repoSection.section, repoSection.output))
                    print_table(table, print_msg.replace("Adding", "Added"))



            output = ok(padding=len(repoSection.section.headertext)) if found else nok(padding=len(repoSection.section.headertext))
        
        
            table = add_and_print(table, f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        if nav:
            add_repo_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()

        
    generate_docs_nav_file("", 1, include_parent_nav=False)


