# Divio Docs Parser

Collect and parse all your [divio-style documentation](https://documentation.divio.com/) with just one line of code! This script will scan any files/directories/strings you pass. For example:
- If you have a how-to section in your README, that'll get extracted and put in the right spot
- Or, if you have an how-to.md file, it'll get added in its entirety!

## How-To
### Install from pip
```bash
python3 -m pip install divio_docs_parser
```

### Clone & run scripts locally
```bash
python3 -m pip install -r requirements.txt
python3 -m src.divio_docs_parser
```

### Run tests
```bash
git clone https://github.com/Denperidge-Redpencil/divio-docs-parser.git
cd divio-docs-gen/src/
python3 -m unittest
```

### Build & install package locally
```bash
git clone https://github.com/Denperidge-Redpencil/divio-docs-parser.git
cd divio-docs-gen/
python3 -m pip install --upgrade build setuptools
python3 -m build && python3 -m pip install --force-reinstall ./dist/*.whl
```
*Note: other Python versions can be used!*


## Explanation
The Divio structure is built upon splitting your documentation into 4 types of documentations. ![The overview of the divio documentation on their website](https://documentation.divio.com/_images/overview.png). In this repository they're referred to as sections.


If you want to know more about the design principles of this project, feel free to check out my writeup [here](https://github.com/Denperidge-Redpencil/Learning.md/blob/main/Notes/docs.md#design-principles)!


## Reference
### Synonyms
For ease of use and freedom of implementation, every section has synonyms.

| Section       | Synonyms                        |
| ------------- | ------------------------------- |
| Tutorials     | Getting started                 |
| How-to Guides | How-To, Guide, Usage            |
| Explanation   | Discussion, background material | 
| Reference     | Technical                       |

