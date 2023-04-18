# Native imports
from configparser import ConfigParser
from os import getcwd, path
from argparse import ArgumentParser

"""Code to handle configuration, through docs.conf or args"""

""" Command-line args """
parser = ArgumentParser()

conf_sections = {
    "output": "Output Configuration", 
    "naming": "Naming Scheme", 
    "repos": "Repository Selection"
    }
ouptut_config = parser.add_argument_group(conf_sections["output"])
ouptut_config.add_argument("--save-conf",
                    dest="SaveConf",
                    help="When used, save the current command line options into ./docs.conf", 
                    action="store_true",
                    default=None,  # store_true default is False
                    )
ouptut_config.add_argument("--generate-nav", "--nav",
                    dest="GenerateNav",
                    help="When used, add internal navigation to the top of each generated file", 
                    action="store_true",
                    default=None,
                    )
ouptut_config.add_argument("--docs-base-dir", "--docs-dir", "--dir", "-d",
                    dest="DocsBasedir",
                    help="What folder to output the docs in. Defaults to `docs/", 
                    )
ouptut_config.add_argument("--write-to-disk", "--write",
                           dest="WriteToDisk",
                           help="Whether to write the markdown to disk",
                           action="store_true",
                           default=None,
                           )

naming_scheme = parser.add_argument_group(conf_sections["naming"])
for section_key in ["tutorials", "how-tos", "explanations", "references"]:
    short_hand = section_key[0] if section_key[0] != "h" else "ht"
    naming_scheme.add_argument(f"--{section_key}", f"-{short_hand}", 
                        dest=section_key,
                        help=f"Sets the output folder name for {section_key}. Defaults to `{section_key}`"
                        )

repo_selection = parser.add_argument_group(conf_sections["repos"])
repo_selection.add_argument("--defaultowner", "--owner", "-do", "-o", 
                    dest="DefaultOwner",
                    help="Defines which user or org has to be checked for the repository in case its Path does not explicitly define an owner")

repo_selection.add_argument("--repo",
                            help="""
                            Configures if/how a repo should be parsed

                            Syntax: OWNER/REPO_NAME [options]
                            Example: denperidge-redpencil/project move=docs/reference/documentation.md

                            If none are defined, all repos will be used.
                            Options:
                            - Copy (array): Files in the repository that should be copied to a specific section. Syntax: move=file.md/sectionname,file2.md/sectionname
                            - Ignore (array) Files in the repository that should be ignored. Syntax: move=file.md,file2.md
                            """,
                            action="append",
                            dest="repos",
                            nargs="*")

args = parser.parse_args()


args_save_conf = bool(getattr(args, "SaveConf")) if hasattr(args, "SaveConf") else False

""" Conf file """
conf_file = path.join(getcwd(), "docs.conf")
use_conf = path.exists(conf_file)
if use_conf or args_save_conf:
    conf = ConfigParser()
    if use_conf:
        conf.read("docs.conf")
    
    for section_key in conf_sections:
        section = conf_sections[section_key]
        if section not in conf:
            conf.add_section(section)


""" Apply & save """
def get_conf_value(section_id, value_id):
    return conf[section_id][value_id] if value_id in conf[section_id] else ""

def get_arg_value(value_id):
    print(args)
    return getattr(args, value_id) if hasattr(args, value_id) else None

def get_value(section_id, value_id, default):
    """Gets the arg, whether it be from the config file or CLI"""
    # Get the value from cli if defined. Cli > conf
    value = get_arg_value(value_id)
    # If it's undefined in the CLI, check if conf can be used
    if value is None and use_conf:
        value = get_conf_value(section_id, value_id)
    elif value is None:
        value = default

    if args_save_conf:
        # If it should be saved, do that
        conf[section_id][value_id] = str(value)
        
    return value

args_default_owner = get_value(conf_sections["repos"], "DefaultOwner", None)  # Used as default repo owner
args_write_to_disk = bool(get_value(conf_sections["output"], "WriteToDisk", False))
args_generate_nav = bool(get_value(conf_sections["output"], "GenerateNav", False))
args_docs_basedir = get_value(conf_sections["output"], "DocsBasedir", "docs/")

args_section_names = dict()
for section_name in ["tutorials", "how-tos", "explanations", "references"]:
    args_section_names[section_name] = get_value(conf_sections["naming"], value_id=section_name, default=section_name).lower()
print(args_section_names)

args_repoconfigs = []
if get_arg_value("repos"):
    for repo_arg in get_arg_value("repos"):
        repo = dict()
        repo["path"] = repo_arg[0]
        for arg in repo_arg[1:]:
            key, value = arg.split("=", 1)
            repo[key] = value
        args_repoconfigs.append(repo)
        conf[repo["path"]] = repo
    
if use_conf:
    all_conf_sections = conf.sections()
    for conf_section_id in all_conf_sections:
        if conf_section_id in conf_sections.values(): continue
        

        conf_section = conf[conf_section_id]
        repo = dict(conf_section)
        if repo not in args_repoconfigs:
            args_repoconfigs.append(repo)
        

if args_save_conf:
    with open("docs.conf", mode="w", encoding="UTF-8") as configfile:
        conf.write(configfile)
