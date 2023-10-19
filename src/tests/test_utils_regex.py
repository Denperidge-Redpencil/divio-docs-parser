import unittest

from ..divio_docs_parser.utils.regex import regex_search, search_ignorecase_multiline, search_ignorecase_multiline_dotallnewline, grab_relative_hrefs


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


    def test_search_relative_hrefs(self):
        haystack="""
![SHOULD BE FOUND](../../assets/image.svg)

![SHOULD BE FOUND](/image.png)

#### In-depth
![SHOULD BE FOUND](../../assets/simple-mental-model-advanced.excalidraw.svg)
[SHOULD NOT BE FOUND](#micro), [centralised communication](#centralised-communication)
[SHOULD NOT BE FOUND](https://mu.semte.ch/2017/06/15/semantic-micro-services-why-bother/)*
[SHOULD BE FOUND](https.mu.semte.ch.md)*
[SHOULD NOT BE FOUND](http://mu.semte.ch/2017/06/15/semantic-micro-services-why-bother/)*
[SHOULD BE FOUND](test.png)
"""

        should_be_found_amount = haystack.count("SHOULD BE FOUND")
        
        hrefs = grab_relative_hrefs(haystack)

        self.assertEqual(len(hrefs), should_be_found_amount)
        for href in hrefs:
            self.assertFalse("SHOULD NOT BE FOUND" in href["title"])



if __name__ == "__main__":
    unittest.main()