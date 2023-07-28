import unittest

from divio_docs_parser.Section import Section
from re import findall, RegexFlag

test_section_name = "tutorials"
test_section_regex = r"tutorial"

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

        results_with_default_regex = findall(self.section.regex, string_with_markdown_headers, RegexFlag.M)
        results_with_md_regex = findall(self.section.regex_with_md_header, string_with_markdown_headers, RegexFlag.M | RegexFlag.I)

        self.assertGreater(len(results_with_default_regex), 1)
        self.assertEqual(len(results_with_md_regex), 1)
    
    
    def test_find_in(self):
        pass


if __name__ == "__main__":
    unittest.main()