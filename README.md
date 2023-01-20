conflicting repo names: merge

We could make the dedicated repo be partially auto-generated into the following structure
/{reponame}
    /tutorials
    /how-tos
    /explanations
    /references

(I will be referring to [tutorials, how-tos, explanations, references] as sections)

This would make things as simple as programatically looping over the repos and importing the markdown files.
Programming it right would allow complete freedom in how this is implemented in the repo.
- Check the README.md section headers. Import contents until the next header of the equivalent
- Otherwise, traverse the git repo for **/*.md, repeating the import from above on every file