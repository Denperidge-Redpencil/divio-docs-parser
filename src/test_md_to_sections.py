import unittest

from divio_docs_parser.md_to_sections import parse_all_sections_from_markdown, _parse_all_sections_from_markdown_file, _parse_all_sections_from_markdown_string


expected_output = {
    "tutorials": 
        """# Tutorials
This is the tutorial text!

## And a subtitle
With more text!

""",

    "how_to_guides":"""# How to
How to...

""",

    "explanation": """# Discussions
...discuss...

""",

    "reference": """# Reference
... data and stuff
"""
}


test_data_path = "tests/test_data/README.md"

class TestDivioDocs(unittest.TestCase):
    
    def test_parse_all_sections_from_markdown_file(self):
        data = _parse_all_sections_from_markdown_file(test_data_path)
        self.assertDictEqual(data, expected_output)
        
       
    def test_parse_all_sections_from_markdown_string(self):
        with open(test_data_path, "r", encoding="utf-8") as file:
            input = file.read()

        data = _parse_all_sections_from_markdown_string(input)
        self.assertDictEqual(data, expected_output)

    
    def test_parse_all_sections_from_either(self):
        with open(test_data_path, "r", encoding="utf-8") as file:
            test_data_string = file.read()

        inputs = [test_data_path, test_data_string]
        for input in inputs:
            data = parse_all_sections_from_markdown(input)
            self.assertDictEqual(data, expected_output)



if __name__ == "__main__":
    unittest.main()