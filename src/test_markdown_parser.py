import unittest

from divio_docs_parser.markdown_parser import parse_all_sections_from_markdown, _parse_all_sections_from_markdown_file, _parse_all_sections_from_markdown_string


expected_output = {
    "tutorials": 
        """# Tutorials
This is the tutorial text!

## And a subtitle
With more text!""",

    "how_to_guides":"""# Howtoguides
How to...
""",

    "discussions": """# Discussions
...discuss...""",

    "reference": """# Reference
... data and stuff"""
}


test_data = "tests/test_data/README.md"

class TestDivioDocs(unittest.TestCase):
    
    def test_parse_all_sections_from_markdown_file(self):
        data = parse_all_sections_from_markdown(test_data)
        print()
        print(data)
        print(expected_output)

        self.assertDictEqual(data, expected_output)
        
       


if __name__ == "__main__":
    unittest.main()