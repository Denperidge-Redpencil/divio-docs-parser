import unittest

from divio_docs_parser.DivioDocs import DivioDocs
from divio_docs_parser.constants import ID_TUTORIALS

readme_path = "tests/test_data/README.md"

readme_tutorials = """# Tutorials
This is the tutorial text!

## And a subtitle
With more text!

"""


class TestDivioDocs(unittest.TestCase):
    
    def test_empty_init(self):
        docs = DivioDocs()
        
        self.assertDictEqual(docs.tutorials, {})
        self.assertDictEqual(docs.how_to_guides, {})
        self.assertDictEqual(docs.explanation, {})
        self.assertDictEqual(docs.reference, {})

    def test_init_with_input(self):
        docs = DivioDocs(readme_path)

        self.assertEqual(docs.tutorials["README.md"], readme_tutorials)
        


    def test_get(self):
        docs = DivioDocs()
        docs.tutorials = {"README.md": "Data"}
        self.assertEqual(docs.get(ID_TUTORIALS, "README.md"), "Data")

    def test_set_undefined_key(self):
        docs = DivioDocs()
        docs.set(ID_TUTORIALS, "README.md", "New data")
        
        self.assertEqual(docs.tutorials["README.md"], "New data")

    def test_set_existing_key(self):
        docs = DivioDocs()
        docs.tutorials = {"README.md": "old data"}
        docs.set(ID_TUTORIALS, "README.md", "New data")
        
        self.assertEqual(docs.get(ID_TUTORIALS, "README.md"), "New data")

    def test_append(self):
        docs = DivioDocs()
        docs.tutorials = {"README.md": "123"}
        docs.append(ID_TUTORIALS, "README.md", "456")

        self.assertEqual(docs.get(ID_TUTORIALS, "README.md"), "123456")

    def test_prepend(self):
        docs = DivioDocs()
        docs.tutorials = {"README.md": "456"}
        docs.prepend(ID_TUTORIALS, "README.md", "123")

        self.assertEqual(docs.get(ID_TUTORIALS, "README.md"), "123456")

    def test_joined(self):
        docs = DivioDocs()
        docs.tutorials = {"README.md": "123", "Tutorials.md": "456"}

        joined = docs.joined(ID_TUTORIALS)
        self.assertListEqual(joined, ["123", "456"])
    

    def test_import_docs(self):
        docs = DivioDocs().import_docs(readme_path)

        self.assertEqual(docs.tutorials["README.md"], readme_tutorials)


if __name__ == "__main__":
    unittest.main()