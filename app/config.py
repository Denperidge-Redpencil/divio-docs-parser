from configparser import ConfigParser

conf = ConfigParser()
conf.read("docs.conf")


def get_conf_value(section_id, value_id, default=None):
    return conf[section_id][value_id] if value_id in conf[section_id] else default

fallbackOwner = get_conf_value("DEFAULT", "FallbackOwner", None)  # Used as default repo owner
nav = bool(get_conf_value("DEFAULT", "GenerateNav", False))
docs_basedir = get_conf_value("DEFAULT", "DocsBasedir", "docs/")

section_names = dict()
for section_name in ["tutorials", "how-tos", "explanations", "references"]:
    section_names[section_name] = get_conf_value("DEFAULT", value_id=section_name, default=section_name).lower()

repopaths = []
conf_sections = conf.sections()
for conf_section_id in conf_sections:
    conf_section = conf[conf_section_id]
    repopaths.append(conf_section['Path'])
