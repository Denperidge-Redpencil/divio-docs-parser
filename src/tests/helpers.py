from pathlib import Path
from os import makedirs, path

from ..divio_docs_parser.constants import *

"""Helpers for the tests"""

tests_dir = Path(path.dirname(__file__)).absolute()

test_data_dir = tests_dir.joinpath("data/")
test_data_extra_dir = test_data_dir.joinpath("extra/")

makedirs(test_data_extra_dir, exist_ok=True)

test_data_readme_path = test_data_dir.joinpath("README.md")
test_data_tutorials_path = test_data_extra_dir.joinpath("Tutorials.md")


TEST_README_CONTENT = \
"""# README.md
## Tutorials
This is the tutorial text!

### And a subtitle
With more text!

## How to
How to...

## Discussions
...discuss...

## Reference
... data and stuff
"""


TEST_README_PARSED = {
    ID_TUTORIALS: 
        """# Tutorials
This is the tutorial text!

## And a subtitle
With more text!

""",

    ID_HOW_TO_GUIDES:"""# How to
How to...

""",

    ID_EXPLANATION: """# Discussions
...discuss...

""",

    ID_REFERENCE: """# Reference
... data and stuff
"""
}

TEST_DATA_TUTORIALS_CONTENT = \
"""# Extra file
## Extra content
For a different test"""


with open(test_data_readme_path, "w", encoding="UTF-8") as file:
    file.write(TEST_README_CONTENT)

with open(test_data_tutorials_path, "w", encoding="UTF-8") as file:
    file.write(TEST_DATA_TUTORIALS_CONTENT)
