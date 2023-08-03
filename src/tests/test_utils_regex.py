import unittest

from ..divio_docs_parser.utils.regex import regex_search, search_ignorecase_multiline, search_ignorecase_multiline_dotallnewline


class TestUtilsRegex(unittest.TestCase):
    def test_basic_string(self):
        needle = "find me!"
        haystack = """
        a string
        where you
        can find me!"""
        
        self.assertIsNotNone(regex_search(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline_dotallnewline(needle, haystack))

    
    def test_inconsistent_case(self):
        needle = "find me!"
        haystack = """
        a string
        where you
        can fIND mE!"""
        
        self.assertIsNone(regex_search(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline_dotallnewline(needle, haystack))

    
    def test_multiline(self):
        needle = "^find me!"
        haystack = """
        a string
        decoy find me! this shouldn't be detected
        where you can
find me!"""
        
        self.assertIsNone(regex_search(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline_dotallnewline(needle, haystack))


    def test_dotallnewline(self):
        needle = "find.*me!"
        haystack = """
        a string
        where you
        can find
        me!"""

        self.assertIsNone(regex_search(needle, haystack))
        self.assertIsNone(search_ignorecase_multiline(needle, haystack))
        self.assertIsNotNone(search_ignorecase_multiline_dotallnewline(needle, haystack))




if __name__ == "__main__":
    unittest.main()