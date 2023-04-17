# Divio Docs Generator

Automatically collect, aggregate and structure all your [divio-style documentation](https://documentation.divio.com/) into a tree of .md files.
```
/{reponame}
    /tutorials
    /how-tos
    /explanations
    /references
```

- Any input structure: this script will scan your entire repository for .md files
    - If you have a how-to section in your README, that'll get extracted and put in the right spot
    - Or, if you have an how-to.md file, it'll get added in its entirety!
- Any output structure: this script generates a simple markdown tree. Nothing proprietary, no vendor-lockin. It can be generated from GitHub Actions and put into a Jekyll pages site just as easily as it is run from a Raspberry Pi and used to render the contents of an Ember application.

All you have to do is simply name your headers and/or files after the divio sections (`tutorial`, `how-to`, `explanation`, `reference`). (Oh, don't worry, the search is done through a case insensitive regex. Add more words as you please) 

## Getting-Started / tutorial
*(You can also use the [repository template](https://github.com/Denperidge-Redpencil/Divio-Docs-Repo/)!)*

- Clone the repository using `git clone https://github.com/Denperidge-Redpencil/divio-docs-gen.git && cd divio-docs-gen`
- Install the pre-requirements using `python3 -m pip install -r requirements.txt`
- Setup the docs.conf file (See the [reference below](#docsconf) and/or the [docs.conf.example](docs.conf.example) file)
- And finally, run using `python3 app/index.py`!

## How-To
### Build & install package locally
```bash
python3.10 -m pip install --upgrade build setuptools
python3.10 -m build
python3.10 -m pip install --force-reinstall ./dist/*.whl
```
*Note: other Python versions can be used!*

## Discussions
The Divio structure is built upon splitting your documentation into 4 types of documentations. ![The overview of the divio documentation on their website](https://documentation.divio.com/_images/overview.png). In this repository they're referred to as sections.


If you want to know more about the design principles of this project, feel free to check out my writeup [here](https://github.com/Denperidge-Redpencil/Learning.md/blob/main/Notes/docs.md#design-principles)!


## Reference

### docs.conf
#### [DEFAULT] section
This section is on the top of the file, and defines options that affect the entire configuration
| Parameter     | Functionality                    |
| ------------- | -------------------------------- |
| DefaultOwner | (string) Defines which user or org has to be checked for the repository in case its Path does not explicitly define an owner |
| GenerateNav   | (boolean) Whether to add internal navigation to the top of each generated file. Defaults to `False` |
| DocsBasedir   | What folder to output the docs in. Defaults to `docs/` |
| Tutorials     | Sets the output folder name for tutorials. Defaults to `tutorials`    |
| How-tos       | Sets the output folder name for how-tos. Defaults to `how-tos`    |
| explanations  | Sets the output folder name for explanations. Defaults to `explanations`    |
| references    | Sets the output folder name for references. Defaults to `references`    |


#### [repo] section
You can add as many of these as you want. Each one represents a repo you want parsed. You can give any name to `[the-section-header]`, but you should probably avoid duplicates. If no repo sections are defined but you've defined DefaultOwner, all repos of that user or organisation will be parsed.

| Parameter | Functionality                              |
| --------- | ------------------------------------------ |
| Path      | (string) Defines which repository to parse |
| Copy      | (array) Files in the repository that should be copied to a specific section. Syntax: `file.md/sectionname,file2.md/sectionname` |
| Ignore      | (array) Files in the repository that should be ignored. Syntax: `file.md,file2.md` |

*Note: for `Copy` and `Ignore` you can choose to be more specific by writing `sub/folder/filename.md`. The check is a `provided_path in full_filepath`, so `sub/folder/filename.md` will apply to `even/further/sub/folder/filename.md`.*

##### Allowed Path syntax
You can use any of the following!
- `reponame` (if DefaultOwner is defined)
- `reponame@branch` (if DefaultOwner is defined)
- `owner/reponame`
- `owner/reponame@branch`



### Synonyms
For ease of use and freedom of implementation, every section has synonyms.

| Section       | Synonyms                        |
| ------------- | ------------------------------- |
| Tutorials     | Getting started                 |
| How-To's      | How-To, Guide, Usage            |
| Explanation   | Discussion, background material | 
| Reference     | Technical                       |


