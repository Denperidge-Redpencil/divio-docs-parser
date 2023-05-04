from .Repo import Repo
from .parse import repo_to_divio_docs_entries
from .Section import sections

"""Entrypoint for the application"""

def main():
    print("@@@")
    print(sections)
    repo = Repo("https://github.com/mu-semtech/mu-cl-resources")
    entry = repo_to_divio_docs_entries(repo, True)
    entry.write_to_disk()


if __name__ == "__main__":
    main()
