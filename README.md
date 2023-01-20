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
- Clone the repository using `git clone https://github.com/Denperidge-Redpencil/divio-docs-gen.git && cd divio-docs-gen`
- Install the pre-requirements using `python3 -m pip install -r requirements.txt`
- Setup the .env file (also see the [.env.example](.env.example) file)
    |   name    | value                     |
    | --------- | ------------------------- |
    | repos     | a list of repositories you want to generate docs for, split by `,`. Format: `owner/reponame`, `owner/reponame@branch` or (when userOrOrg is defined) `reponame`/`reponame@branch` |
    | userOrOrg | username or organisation name. Setting this allows you to omit the owner whilst defining repos |
- And finally, run using `python3 app/index.py`!


## Reference
If you want to know more about the design principles of this project, feel free to check out my writeup [here](https://github.com/Denperidge-Redpencil/Learning.md/blob/main/Notes/docs.md#design-principles)!
