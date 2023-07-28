import unittest

from divio_docs_parser.Section import Section
from re import findall, RegexFlag

test_section_name = "tutorials"
test_section_regex = r"tutorials"
test_string_with_tutorials = """
## How-to
...

## Tutorials
...

## Reference
...
"""

test_string_without_tutorials = """
## How-to
...

## Reference
...
"""


class TestDivioDocs(unittest.TestCase):
    def setUp(self) -> None:
        self.section = Section(test_section_name, test_section_regex)
    
    def tearDown(self) -> None:
        self.section = None
        
    
    def test_init(self):
        self.assertEqual(self.section.name, test_section_name)
        self.assertEqual(self.section.regex, test_section_regex)

    def test_regex_with_md_header(self):
        string_with_markdown_headers = """### tutorials
            
            This instance of the word "tutorials" should not be caught
            """

        results_with_default_regex = findall(self.section.regex, string_with_markdown_headers, RegexFlag.M | RegexFlag.I)
        results_with_md_regex = findall(self.section.regex_with_md_header, string_with_markdown_headers, RegexFlag.M | RegexFlag.I)

        self.assertGreater(len(results_with_default_regex), 1)
        self.assertEqual(len(results_with_md_regex), 1)
    
    
    def test_find_header(self):
        self.assertIsNotNone(self.section.find_header(test_string_with_tutorials), True)
        self.assertIsNone(self.section.find_header(test_string_without_tutorials), True)

    def test_found_header(self):
        self.assertTrue(self.section.find_header(test_string_with_tutorials), True)
        self.assertFalse(self.section.find_header(test_string_without_tutorials), True)

    def test_found_header(self):
        self.assertTrue(self.section.find_header(test_string_with_tutorials), True)
        self.assertFalse(self.section.find_header(test_string_without_tutorials), True)

    def test_get_header_string(self):
        self.assertEqual(self.section._get_header_string(test_string_with_tutorials), "## Tutorials")
        self.assertIsNone(self.section._get_header_string(test_string_without_tutorials))
    
    def test_get_header_tags_from_string(self):
        self.assertEqual(self.section._get_header_tags_from_string(test_string_with_tutorials), "## ")
    

if __name__ == "__main__":
    unittest.main()