from os import environ
from pathlib import Path
from re import search

from repo import get_repos, Repo
from colourstring import ok, nok
from sections import sections, RepoSection
from table import setup_table, add_and_print, print_table
from docsgen import add_to_docs, add_repo_nav_to_files, generate_docs_nav_file, clear_docs
from config import repopaths, fallbackOwner, nav

if __name__ == "__main__":
    headers = [
        "     repository     ", 
        sections['tutorials'].headertext, sections['howtos'].headertext,
        sections['explanations'].headertext, sections['references'].headertext]

    table = setup_table(headers)

    print_table(table, "Checking repos for divio docs structure...")


    repos_data = get_repos(fallbackOwner) 
    if len(repopaths) > 0:
        repos: list = [ Repo(repos_data, repo, owner=fallbackOwner) for repo in repopaths ]
    elif fallbackOwner:
        # If user is defined but no specific repos, get repos from GitHub API
        repos = [Repo(repos_data, reponame=repo['name'], owner=fallbackOwner, branch=repo['default_branch']) for repo in repos_data]
    else:
        raise ValueError("Either FallbackOwner has/repo Paths have to be defined")
            
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
                # Once found, don't allow found to be reset to false by the folowing files
                if found == False:
                    found = True if section_in_content or section_in_filename else False

                if section_in_content or section_in_filename:
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

            padding = len(repoSection.section.headertext)
            output = ok(padding=padding) if found else nok(padding=padding)

            table = add_and_print(table, f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        if nav and len(created_files) > 0:
            add_repo_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()

        
    generate_docs_nav_file("", 1, include_parent_nav=False)


