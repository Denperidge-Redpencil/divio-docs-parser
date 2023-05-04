from .repo import Repo
from .parse import parse_docs

"""Entrypoint for the application"""


def markdown_to_divio_docs():
    """When given a markdown string, parse and return the data, optionally writing to files"""
    pass

def main():
    repo = Repo("https://github.com/mu-semtech/mu-cl-resources")
    print(parse_docs(repo))



if __name__ == "__main__":
    main()
