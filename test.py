import unittest

from src.tests.test_DivioDocs import TestDivioDocs
from src.tests.test_Section import TestSection
from src.tests.test_utils_files import TestUtilsFiles
from src.tests.test_utils_markdown_parser import TestUtilsMarkdownParser
from src.tests.test_utils_regex import TestUtilsRegex


if __name__ == "__main__":
    suites = []
    for suite in [
        TestDivioDocs,
        TestSection,
        TestUtilsFiles,
        TestUtilsMarkdownParser,
        TestUtilsRegex
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()