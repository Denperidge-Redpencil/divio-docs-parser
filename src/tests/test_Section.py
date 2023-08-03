import unittest

from ..divio_docs_parser.Section import Section
from ..divio_docs_parser.constants import ID_TUTORIALS
from re import findall, RegexFlag

test_section_name = ID_TUTORIALS
test_section_regex = r"tutorials"
test_string_with_tutorials = """
## How-to
...

## Tutorials
### Part 1
Tutorials content

### Part 2
More content

## Reference
...
"""

test_string_without_tutorials = """
## How-to
...

## Reference
...
"""


class TestSection(unittest.TestCase):
    def setUp(self) -> None:
        self.section = Section(test_section_name, test_section_regex)
    
    def tearDown(self) -> None:
        self.section = None
        
    
    def test_init(self):
        self.assertEqual(self.section.id, test_section_name)
        self.assertEqual(self.section.regex, test_section_regex)

    def test_regex_with_md_header(self):
        string_with_markdown_headers = """### tutorials
            
            This instance of the word "tutorials" should not be caught
            """

        results_with_default_regex = findall(self.section.regex, string_with_markdown_headers, RegexFlag.M | RegexFlag.I)
        results_with_md_regex = findall(self.section.regex_with_md_header, string_with_markdown_headers, RegexFlag.M | RegexFlag.I)

        self.assertEqual(len(results_with_default_regex), 2)
        self.assertEqual(len(results_with_md_regex), 1)

    def test_header_from(self):
        self.assertEqual(self.section._header_from(test_string_with_tutorials), "## Tutorials")
        self.assertIsNone(self.section._header_from(test_string_without_tutorials))

        self.assertIsNone(self.section._header_from("path/to/tutorials.md", must_have_header_tags=True))
        self.assertIsNotNone(self.section._header_from("path/to/tutorials.md", must_have_header_tags=False))
    
    def test_header_in(self):
        self.assertTrue(self.section.header_in(test_string_with_tutorials))
        self.assertFalse(self.section.header_in(test_string_without_tutorials))

        self.assertFalse(self.section.header_in("path/to/tutorials.md", must_have_header_tags=True))
        self.assertTrue(self.section.header_in("path/to/tutorials.md", must_have_header_tags=False))


    def test_get_header_tags_from(self):
        self.assertEqual(self.section._header_tags_from(test_string_with_tutorials), "## ")
    
    def test_get_section_content_from_string(self):
        self.assertEqual(self.section._content_from(test_string_with_tutorials),"""\n### Part 1
Tutorials content

### Part 2
More content

""")
                         
    def test_parse_from(self):
        self.assertEqual(self.section.parse_from(test_string_with_tutorials), """# Tutorials
## Part 1
Tutorials content

## Part 2
More content

""")


if __name__ == "__main__":
    unittest.main()