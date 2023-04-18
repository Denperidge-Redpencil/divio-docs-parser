# Native imports
from configparser import ConfigParser
from os import getcwd, path
from argparse import ArgumentParser

"""Code to handle configuration, through docs.conf or args"""

""" Command-line args """
parser = ArgumentParser()

ouptut_config = parser.add_argument_group("Output configuration")
ouptut_config.add_argument("--save-conf", 
                    help="When used, save the current command line options into ./docs.conf", 
                    action="store_true")
ouptut_config.add_argument("--generate-nav", "--nav", 
                    help="When used, add internal navigation to the top of each generated file", 
                    action="store_true")
ouptut_config.add_argument("--docs-base-dir", "--docs-dir", "--dir", "-d", 
                    help="What folder to output the docs in. Defaults to `docs/", 
                    default="docs/")
ouptut_config.add_argument("--write-to-disk", "--write",
                           help="Whether to write the markdown to disk",
                           action="store_true")

naming_scheme = parser.add_argument_group("Naming scheme")
for section in ["tutorials", "how-tos", "explanations", "references"]:
    short_hand = section[0] if section[0] != "h" else "ht"
    naming_scheme.add_argument(f"--{section}", f"-{short_hand}", 
                        help=f"Sets the output folder name for {section}. Defaults to `{section}`", 
                        default=section)

repo_selection = parser.add_argument_group("Repository selection")
repo_selection.add_argument("--defaultowner", "--owner", "-do", "-o", 
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

""" Conf file """
conf_file = path.join(getcwd(), "docs.conf")
use_conf = path.exists(conf_file)
if use_conf:
    conf = ConfigParser()
    conf.read("docs.conf")

def get_conf_value(section_id, value_id):
    return conf[section_id][value_id] if value_id in conf[section_id] else ""

def get_arg_value(value_id):
    return getattr(args, value_id) if hasattr(args, value_id) else ""

def get_value(section_id, value_id, default):
    """Gets the arg, whether it be from the config file or CLI"""
    value = get_conf_value(section_id, value_id) if use_conf else get_arg_value(value_id.lower())
    return value if value != "" else default

args_default_owner = get_value("DEFAULT", "DefaultOwner", None)  # Used as default repo owner
args_generate_nav = bool(get_value("DEFAULT", "GenerateNav", False))
args_docs_basedir = get_value("DEFAULT", "DocsBasedir", "docs/")
args_write_to_disk = bool(get_value("DEFAULT", "WriteToDisk", False))

args_section_names = dict()
for section_name in ["tutorials", "how-tos", "explanations", "references"]:
    args_section_names[section_name] = get_value("DEFAULT", value_id=section_name, default=section_name).lower()


args_repoconfigs = []
if use_conf:
    conf_sections = conf.sections()
    for conf_section_id in conf_sections:
        conf_section = conf[conf_section_id]
        args_repoconfigs.append(dict(conf_section))
else:
    for repo_arg in get_arg_value("repos"):
        repo = dict()
        repo["path"] = repo_arg[0]
        for arg in repo_arg[1:]:
            key, value = arg.split("=", 1)
            repo[key] = value
        args_repoconfigs.append(repo)

