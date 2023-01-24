from os import environ
from pathlib import Path
from re import search

from dotenv import load_dotenv

from repo import get_repos, get_file_contents, download_and_unzip, Repo
from colourstring import ok, nok
from sections import sections, RepoSection, Section
from table import setup_table, add_and_print, print_table
from docsgen import add_to_docs, add_repo_nav_to_files, generate_docs_nav_file, clear_docs

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
    repos_data = get_repos(userOrOrgFallback) 
    try:
        reponames = environ.get('REPOS').split(',')
        repos: list = [ Repo(repos_data, repo, owner=userOrOrgFallback) for repo in reponames ]

    except AttributeError:
        # If user is defined but no specific repos, get repos from GitHub API
        if userOrOrgFallback:
            repos = [Repo(repos_data, reponame=repo['name'], owner=userOrOrgFallback, branch=repo['default_branch']) for repo in repos_data]
            
            
    clear_docs(sections)


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

                # If the file is a section-specific file
                section_in_filename =  repoSection.section.found_in(filename)
                # If the section can be found in a general file
                section_in_content = repoSection.section.found_in(file_content, header=True)

                # Written longer than needed for clarity
                found = True if section_in_content or section_in_filename else False

                if found:
                    repoSection.sourceContent = file_content

                    # If found in filename, add the raw output
                    # If found within a files content, add the (filtered) output to docs
                    location, content_to_add = \
                        ("filename", file_content) if section_in_filename \
                        else ("filecontent", repoSection.output)

                    print_msg = f"Adding {repo.name} - {repoSection.section.name} from {location}"

                    print_table(table, print_msg)

                    created_files.append(add_to_docs(repo.name, repoSection.section, file_content, filename=Path(filename).name))
                    print_table(table, print_msg.replace("Adding", "Added"))


            output = ok(padding=len(repoSection.section.headertext)) if found else nok(padding=len(repoSection.section.headertext))
        
        
            table = add_and_print(table, f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        if nav and len(created_files) > 0:
            add_repo_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()

        
    generate_docs_nav_file("", 1, include_parent_nav=False)


