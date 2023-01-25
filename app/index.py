from pathlib import Path

from repo import get_repos, Repo
from colourstring import ok, nok
from sections import sections, RepoSection
from table import setup_table, add_and_print, print_table, log_and_print, change_log_index
from docsgen import add_to_docs, add_repo_nav_to_files, generate_docs_nav_file, clear_docs
from config import repopaths, fallbackOwner, nav



if __name__ == "__main__":
    headers = [
        "     repository     ", 
        sections['tutorials'].headertext, sections['howtos'].headertext,
        sections['explanations'].headertext, sections['references'].headertext]

    setup_table(headers)

    log_and_print("Collecting Repo data...")
    change_log_index(+1)

    log_and_print("Collecting repos_data json...")
    change_log_index(+1)
    repos_data = get_repos(fallbackOwner)
    change_log_index(-1)
    log_and_print("... collected repos_data")

    if len(repopaths) > 0:
        log_and_print("Using repo paths defined in config")
        repos: list = [ Repo(repos_data, repo, owner=fallbackOwner) for repo in repopaths ]
    elif fallbackOwner:
        log_and_print(f"FallbackOwner defined, but no repo paths. Adding all repos owned by {fallbackOwner}")
        # If user is defined but no specific repos, get repos from GitHub API
        repos = [Repo(repos_data, reponame=repo['name'], owner=fallbackOwner, branch=repo['default_branch']) for repo in repos_data]
    else:
        err_msg = "Either FallbackOwner has/repo Paths have to be defined"
        log_and_print(err_msg)
        raise ValueError(err_msg)

    change_log_index(-1)
    log_and_print("... collected Repo data")
    
    clear_docs(sections)

    log_and_print("Parsing repos...")
    change_log_index(1)
    for repo in repos:
        log_and_print(f"Parsing {repo.owner}/{repo.name}@{repo.branch}...")
        change_log_index(1)
        # Start the row  with the repo name
        repoHeaderLength = len(headers[0])
        reponamePadded = repo.name[:repoHeaderLength].center(repoHeaderLength)
        add_and_print(f"\n| {reponamePadded} |")

        readme_content = repo.filecontents("README.md")

        created_files = []

        # Go over every section
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])
            
            markdown_files = repo.all_markdown_files
            found = False
            log_and_print(f"Looking for {repoSection.section.name} in markdown files...")
            change_log_index(1)
            for filename in markdown_files:
                file_content = repo.filecontents(filename)

                # If the file is a section-specific file
                section_in_filename =  repoSection.section.found_in(filename)
                # If the section can be found in a general file
                section_in_content = repoSection.section.found_in(file_content, header=True)

                # Once found, don't allow found to be reset to false by the folowing files
                if found == False:
                    # Written longer than needed for clarity
                    found = True if section_in_content or section_in_filename else False

                if section_in_content or section_in_filename:
                    log_and_print("")
                    log_and_print(f"Found section {repoSection.section.name}, handling {filename}...")
                    change_log_index(+1)

                    log_and_print(f"Section in content: {section_in_content}")
                    log_and_print(f"Section in filename: {section_in_filename}")

                    repoSection.sourceContent = file_content

                    # If found in filename, add the raw output
                    # If found within a files content, add the (filtered) output to docs
                    location, content_to_add = \
                        ("filename", file_content) if section_in_filename \
                        else ("filecontent", repoSection.output)

                    print_msg = f"Adding {repo.name} - {repoSection.section.name} section from {location}"

                    log_and_print(print_msg)

                    created_files.append(add_to_docs(repo.name, repoSection.section, content_to_add, filename=Path(filename).name))
                    log_and_print(print_msg.replace("Adding", "Added"))

                    change_log_index(-1)
                    log_and_print(f"...finished handling {filename}")
                    log_and_print("")
                else:
                    log_and_print(f"Section {repoSection.section.name} not found in {filename}")
                
            change_log_index(-1)
            log_and_print(f"... finished looking for {repoSection.section.name} in markdown files")

            padding = len(repoSection.section.headertext)
            output = ok(padding=padding) if found else nok(padding=padding)

            add_and_print(f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        if nav and len(created_files) > 0:
            add_repo_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()
        change_log_index(-1)
        log_and_print(f"... parsed {repo.name}\n")


    change_log_index(-1)
    log_and_print("... finished parsing repos")

        
    generate_docs_nav_file("", 1, include_parent_nav=False)


