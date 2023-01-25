from pathlib import Path

from repo import get_repos, Repo
from colourstring import ok, nok
from sections import sections, RepoSection
from table import setup_table, add_and_print, print_table, log_and_print
from docsgen import add_to_docs, add_repo_nav_to_files, generate_docs_nav_file, clear_docs
from config import repopaths, fallbackOwner, nav



if __name__ == "__main__":
    headers = [
        "     repository     ", 
        sections['tutorials'].headertext, sections['howtos'].headertext,
        sections['explanations'].headertext, sections['references'].headertext]

    setup_table(headers)

    log_and_print("Collecting Repo data...")

    log_and_print("Calling GitHub API...", 1)
    repos_data = get_repos(fallbackOwner)
    log_and_print("... called GitHub API", 1)

    if len(repopaths) > 0:
        log_and_print("Using repo paths defined in config", 1)
        repos: list = [ Repo(repos_data, repo, owner=fallbackOwner) for repo in repopaths ]
    elif fallbackOwner:
        log_and_print(f"FallbackOwner defined, but no repo paths. Adding all repos owned by {fallbackOwner}", 1)
        # If user is defined but no specific repos, get repos from GitHub API
        repos = [Repo(repos_data, reponame=repo['name'], owner=fallbackOwner, branch=repo['default_branch']) for repo in repos_data]
    else:
        err_msg = "Either FallbackOwner has/repo Paths have to be defined"
        log_and_print(err_msg)
        raise ValueError(err_msg)

    log_and_print("... collected Repo data")
    
    log_and_print("Clearing old docs")
    clear_docs(sections)
    log_and_print("Cleared old docs")

    log_and_print("Parsing repos...")
    for repo in repos:
        log_and_print(f"Parsing {repo.name}...", 1)
        # Start the row  with the repo name
        repoHeaderLength = len(headers[0])
        reponamePadded = repo.name[:repoHeaderLength].center(repoHeaderLength)
        add_and_print(f"\n| {reponamePadded} |", f"Checking {repo.name}...")

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

                    print_table(print_msg)

                    created_files.append(add_to_docs(repo.name, repoSection.section, file_content, filename=Path(filename).name))
                    print_table(print_msg.replace("Adding", "Added"))

            padding = len(repoSection.section.headertext)
            output = ok(padding=padding) if found else nok(padding=padding)

            add_and_print(f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        if nav and len(created_files) > 0:
            add_repo_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()
        log_and_print(f"... parsed {repo.name}", 1)

    log_and_print("... finished parsing repos")

        
    generate_docs_nav_file("", 1, include_parent_nav=False)


