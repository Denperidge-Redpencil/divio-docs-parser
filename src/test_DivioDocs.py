import unittest

from divio_docs_parser.DivioDocs import DivioDocs

class TestDivioDocs(unittest.TestCase):
    
    def test_empty_init(self):
        docs = DivioDocs()
        
        self.assertDictEqual(docs.tutorials, {})
        self.assertDictEqual(docs.how_to_guides, {})
        self.assertDictEqual(docs.explanation, {})
        self.assertDictEqual(docs.reference, {})

    def test_filled_init(self):
        dict = {"README.md": "Readme"}
        docs = DivioDocs(dict, dict, dict, dict)

        self.assertDictEqual(docs.tutorials, dict)
        self.assertDictEqual(docs.how_to_guides, dict)
        self.assertDictEqual(docs.explanation, dict)
        self.assertDictEqual(docs.reference, dict)

    def test_get(self):
        docs = DivioDocs({"README.md": "Data"})
        self.assertEqual(docs.get("tutorials", "README.md"), "Data")

    def test_set_undefined_key(self):
        docs = DivioDocs()
        docs.set("tutorials", "README.md", "New data")
        
        self.assertEqual(docs.get("tutorials", "README.md"), "New data")

    def test_set_existing_key(self):
        docs = DivioDocs({"README.md": "old data"})
        docs.set("tutorials", "README.md", "New data")
        
        self.assertEqual(docs.get("tutorials", "README.md"), "New data")

    def test_append(self):
        docs = DivioDocs({"README.md": "123"})
        docs.append("tutorials", "README.md", "456")

        self.assertEqual(docs.get("tutorials", "README.md"), "123456")

    def test_prepend(self):
        docs = DivioDocs({"README.md": "456"})
        docs.prepend("tutorials", "README.md", "123")

        self.assertEqual(docs.get("tutorials", "README.md"), "123456")

    def test_joined(self):
        docs = DivioDocs({"README.md": "123", "Tutorials.md": "456"})

        joined = docs.joined("tutorials")
        self.assertListEqual(joined, ["123", "456"])


if __name__ == "__main__":
    unittest.main()