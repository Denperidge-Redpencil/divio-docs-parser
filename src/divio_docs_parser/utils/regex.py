from re import search as _search, RegexFlag, sub, escape

def regex_search(needle: r"str", haystack: str, flags=0):
    """Base regex helper"""
    return _search(needle, haystack, flags)

def search_ignorecase_multiline(needle: r"str", haystack: str):
    """Helper for case insensitive & multiline regex"""
    return regex_search(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    
# Includes https://docs.python.org/3/library/re.html#re.S
def search_ignorecase_multiline_dotallnewline(needle: r"str", haystack: str):
    """
    Helper for dotall (. matches newline), case insensitive & multiline regex
    
    For RegexFlag.S, see https://docs.python.org/3/library/re.html#re.S
    """
    return regex_search(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE | RegexFlag.S)

