# Native imports
from pathlib import Path

# Local imports
from .repo import get_repos, Repo
from .colourstring import ok, nok
from .sections import sections, RepoSection
from .table import setup_table, add_and_print, log_and_print, change_log_index
from .docsgen import filepath_in_exceptions, add_to_docs, add_sibling_nav_to_files, generate_docs_nav_file, clear_docs
from .args import args_repoconfigs, args_default_owner, args_generate_nav

"""Entrypoint for the application"""


def generate_docs():    
    # Get headers for CLI table
    headers = [
        "     repository     ", 
        sections['tutorials'].headertext, sections['howtos'].headertext,
        sections['explanations'].headertext, sections['references'].headertext]

    setup_table(headers)

    log_and_print("Collecting Repo data...")
    change_log_index(+1)

    log_and_print("Collecting repos_data json...")
    change_log_index(+1)


    # Get repo data
    repos_data = get_repos(args_default_owner)
    
    
    change_log_index(-1)
    log_and_print("... collected repos_data")

    # If repo paths have been defined in docs.conf, use those
    if len(args_repoconfigs) > 0:
        log_and_print("Using repo paths defined in config")
        repos: list = [ Repo(repos_data, config=repoconfig) for repoconfig in args_repoconfigs ]
    
    # If no repo paths have been defined in docs.conf, use all repos from a specific owner
    elif args_default_owner:
        log_and_print(f"args_default_owner defined, but no repo paths. Adding all repos owned by {args_default_owner}")
        # If user is defined but no specific repos, get repos from GitHub API
        repos = [Repo(repos_data, reponame=repo['name'], owner=args_default_owner, branch=repo['default_branch']) for repo in repos_data]
    
    # However, if no paths NOR default owner has been specified, exit
    else:
        err_msg = "Either args_default_owner has/repo Paths have to be defined"
        log_and_print(err_msg)
        raise ValueError(err_msg)

    change_log_index(-1)
    log_and_print("... collected Repo data")
    
    # Remove previously generated docs
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

        # readme_content = repo.filecontents("README.md")

        # Keep track of created files, in case a nav bar is to be created
        created_files = []

        # Go over every possible section, for every markdown file in the repo
        # 1. Check if they're in there, 
        # 2. Check if they have an exception (see config.py)
        # 3. Add to docs accordingly 
        for i, section_id in enumerate(sections):
            repoSection = RepoSection(sections[section_id])

            markdown_files = repo.all_markdown_files
            found = False
            log_and_print(f"Looking for {repoSection.section.name} in markdown files...")
            change_log_index(1)
            for filepath in markdown_files:
                file_content = repo.filecontents(filepath)
                filename = Path(filepath).name

                # If the file is a section-specific file
                section_in_filename =  repoSection.section.found_in(filepath)
                # If the section can be found in a general file
                section_in_content = repoSection.section.found_in(file_content, header=True)

                # Once found, don't allow found to be reset to false by the folowing files
                if found == False:
                    # Written longer than needed for clarity
                    found = True if section_in_content or section_in_filename else False



                ignore = filepath_in_exceptions(repo.files_to_ignore, filepath)
                copy = filepath_in_exceptions(repo.files_to_copy, filepath)
                if ignore:
                    log_and_print(f"Ignoring {ignore}")
                    continue
                if copy:
                    copy_filename, copy_dest = copy.rsplit("/", 1)
                    copy_filename = Path(copy_filename).name # The selector can be a path, but only the filename should be kept for handling
                    log_and_print(f"Copying {copy_filename} to {copy_dest}")
                    
                    add_to_docs(repo.name, copy_dest, file_content, filename)
                    repo.files_to_copy.remove(copy)
                    repo.files_to_ignore.append(copy_filename)
                    
                    log_and_print(f"{copy_filename}'s content has been copied!")
                    continue
                    


                if section_in_content or section_in_filename:
                    log_and_print("")
                    log_and_print(f"Found section {repoSection.section.name}, handling {filepath}...")
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

                    created_files.append(add_to_docs(repo.name, repoSection.section, content_to_add, filename=filename))
                    log_and_print(print_msg.replace("Adding", "Added"))

                    change_log_index(-1)
                    log_and_print(f"...finished handling {filepath}")
                    log_and_print("")
                else:
                    log_and_print(f"Section {repoSection.section.name} not found in {filepath}")
                
            change_log_index(-1)
            log_and_print(f"... finished looking for {repoSection.section.name} in markdown files")

            padding = len(repoSection.section.headertext)
            output = ok(padding=padding) if found else nok(padding=padding)

            add_and_print(f" {output} |", f"Finished handling {repoSection.section.name}")
        
        
        # If a nav has to be created, do that
        if args_generate_nav and len(created_files) > 0:
            add_sibling_nav_to_files(created_files)
            generate_docs_nav_file(repo.name, 1)

        print()
        change_log_index(-1)
        log_and_print(f"... parsed {repo.name}\n")


    change_log_index(-1)
    log_and_print("... finished parsing repos")

    # Create a top level nav file
    generate_docs_nav_file("", 1, include_parent_nav=False)


if __name__ == "__main__":
    generate_docs()