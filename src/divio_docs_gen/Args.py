# Native imports
from configparser import ConfigParser
from os import getcwd, path
from argparse import ArgumentParser

from .Repo import Repo

"""Code to handle configuration, through docs.conf or args"""

section_keys = ["tutorials", "howtos", "explanations", "references"]
class Args:
    def __init__(self) -> None:
        # store_true default is False, which means save_conf's output will be too verbose. Use None instead
        self.save_conf = None  
        self.write_to_disk = None
        self.docs_basedir = "docs/"
        self.generate_nav = None

        self.tutorials, self.howtos, self.explanations, self.references = section_keys

        self.repos = []
    
    def get_configured_section_name(self, section_id: str):
        # TODO look for a cleaner solution
        if section_id == section_keys[0]:
            return self.tutorials
        elif section_id == section_keys[1]:
            return self.howtos
        elif section_id == section_keys[2]:
            return self.explanations
        elif section_id == section_keys[3]:
            return self.references
        print(section_id)


    
    def __str__(self) -> str:
        return f"""
        Configured args:

        - save_conf: {self.save_conf} 
        - write_to_disk: {self.write_to_disk} 
        - docs_basedir: {self.docs_basedir} 
        - generate_nav: {self.generate_nav}

        - tutorials: {self.tutorials}
        - howtos: {self.howtos}
        - explanations: {self.explanations}
        - references: {self.references}

        - repos: {self.repos} 
        """

    def __repr__(self) -> str:
        return self.__str__()

args = Args()

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
                    default=args.save_conf,  
                    )
ouptut_config.add_argument("--write-to-disk", "--write",
                           dest="WriteToDisk",
                           help="Whether to write the markdown to disk",
                           action="store_true",
                           default=args.write_to_disk,
                           )
ouptut_config.add_argument("--docs-base-dir", "--docs-dir", "--dir", "-d",
                    dest="DocsBasedir",
                    help=f"What folder to output the docs in. Defaults to `{args.docs_basedir}`", 
                    )
ouptut_config.add_argument("--generate-nav", "--nav",
                    dest="GenerateNav",
                    help="When used, add internal navigation to the top of each generated file", 
                    action="store_true",
                    default=args.generate_nav,
                    )
naming_scheme = parser.add_argument_group(conf_sections["naming"])
for section_key in section_keys:
    short_hand = section_key[0] if section_key[0] != "h" else "ht"
    naming_scheme.add_argument(f"--{section_key}", f"-{short_hand}", 
                        dest=section_key,
                        help=f"Sets the output folder name for {section_key}. Defaults to `{section_key}`"
                        )

repo_selection = parser.add_argument_group(conf_sections["repos"])
repo_selection.add_argument("--repo",
                            help="""
                            Configures if/how a repo should be parsed
                            This can be defined multiple times

                            Syntax: --repo git_url
                            Example: denperidge-redpencil/project move=docs/reference/documentation.md

                            If none are defined, all repos will be used.
                            Options:
                            - Copy (array): Files in the repository that should be copied to a specific section. Syntax: move=file.md/sectionname,file2.md/sectionname
                            - Ignore (array) Files in the repository that should be ignored. Syntax: move=file.md,file2.md
                            """,
                            action="append",
                            dest="repos",
                            nargs="*")

cli_args = parser.parse_args()
args.save_conf = bool(getattr(cli_args, "SaveConf")) if hasattr(cli_args, "SaveConf") else False

""" Conf file """
conf_file = path.join(getcwd(), "docs.conf")
use_conf = path.exists(conf_file)
if use_conf or args.save_conf:
    conf = ConfigParser()
    if use_conf:
        conf.read("docs.conf")
    
    for section_key in conf_sections:
        section = conf_sections[section_key]
        if section not in conf:
            conf.add_section(section)


""" Get config, save if desired, apply"""
def get_conf_value(section_id, value_id):
    return conf[section_id][value_id] if value_id in conf[section_id] else ""

def get_cli_arg_value(value_id):
    return getattr(cli_args, value_id) if hasattr(cli_args, value_id) else None

def get_value(section_id, value_id, default):
    """Gets the arg, whether it be from the config file or CLI"""
    # Get the value from cli if defined. Cli > conf
    value = get_cli_arg_value(value_id)
    # If it's undefined in the CLI, check if conf can be used
    if value is None and use_conf:
        value = get_conf_value(section_id, value_id)
    elif value is None:
        value = default

    if args.save_conf:
        # If it should be saved, do that
        conf[section_id][value_id] = str(value)
        
    return value

args.write_to_disk = bool(get_value(conf_sections["output"], "WriteToDisk", False))
args.generate_nav = bool(get_value(conf_sections["output"], "GenerateNav", False))
args.docs_basedir = get_value(conf_sections["output"], "DocsBasedir", "docs/")

for i, section_name in enumerate(["tutorials", "howtos", "explanations", "references"]):
    # TODO cleaner solution
    value = get_value(conf_sections["naming"], value_id=section_name, default=section_name)
    if i == 0:
        args.tutorials = value
    elif i == 1:
        args.howtos = value
    elif i == 2:
        args.explanations = value
    elif i == 3:
        args.references = value


if get_cli_arg_value("repos"):
    for repo_arg in get_cli_arg_value("repos"):
        repo = Repo(repo_arg[0])
        for arg in repo_arg[1:]:
            key, value = arg.split("=", 1)
            key = key.lower()
            if "ignore" in key:
                repo.files_to_ignore.append(value)
            elif "copy" in key:
                repo.files_to_copy.append(value) 

        args.repos.append(repo)
        conf[repo["url"]] = repo
    
if use_conf:
    all_conf_sections = conf.sections()
    for conf_section_id in all_conf_sections:
        if conf_section_id in conf_sections.values(): continue

        conf_section = conf[conf_section_id]
        repo_data = dict(conf_section)
        repo = Repo(repo_data["url"])
        
        if "ignore" in repo_data:
            repo.files_to_ignore.append(repo_data["ignore"])
        if "copy" in repo_data:
            repo.files_to_copy.append(repo_data["copy"])
            

        if repo not in args.repos:
            args.repos.append(repo)
        

if args.save_conf:
    with open("docs.conf", mode="w", encoding="UTF-8") as configfile:
        conf.write(configfile)

print(args)