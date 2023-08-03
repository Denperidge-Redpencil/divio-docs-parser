import unittest
from os import makedirs
from shutil import rmtree

from ..divio_docs_parser.utils.files import list_all_files, list_all_markdown_files

def touch(filename):
    with open(filename, "a"):
        pass

class TestUtilsFiles(unittest.TestCase):
    def setUp(self) -> None:
        self.dirname = "random_dir/"
        furthest_subdir = self.dirname + "files/here/"
        filenames = [
            self.dirname + "test.txt", 
            self.dirname + "test2.md",
            self.dirname + "files/tutorials.md",
            self.dirname + "files/test.txt",
            self.dirname + "files/here/isafile.md"
        ]

        self.generated_files_count = len(filenames)
        self.generated_markdown_files_count = len([filename for filename in filenames if filename.lower().endswith(".md")])

        makedirs(furthest_subdir, exist_ok=True)
        
        for filename in filenames:
            touch(filename)
        
    
    def tearDown(self) -> None:
        rmtree(self.dirname)
    
    def test_list_all_files(self):
        all_files = list_all_files(self.dirname)

        self.assertEqual(len(all_files), self.generated_files_count)
    
    def test_list_all_markdown_files(self):
        found_markdown_files = list_all_markdown_files(self.dirname)

        self.assertEqual(len(found_markdown_files), self.generated_markdown_files_count)




if __name__ == "__main__":
    unittest.main()