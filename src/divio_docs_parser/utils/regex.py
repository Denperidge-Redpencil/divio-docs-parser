from re import search as _search, RegexFlag, sub, escape, findall, compile, finditer

_regex_relative_href = r"(!|)\[(?P<title>.*?)\]\((?!(#|http://|https://))(?P<href>.*?)\)"

def regex_search(needle: r"str", haystack: str, flags=0):
    """Base regex search helper"""
    try:
        return _search(str(needle), str(haystack), flags)
    except TypeError as error:
        raise error


def search_ignorecase_multiline(needle: r"str", haystack: str):
    """Helper for case insensitive & multiline regex"""
    return regex_search(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    
# Includes https://docs.python.org/3/library/re.html#re.S
def search_ignorecase_multiline_dotallnewline(needle: r"str", haystack: str):
    """
    Helper for dotall (. matches newline), case insensitive & multiline regex
    
    For dotall/RegexFlag.S, see https://docs.python.org/3/library/re.html#re.S
    """
    return regex_search(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE | RegexFlag.S)

def grab_relative_hrefs(haystack: str):
    output = []
    results = finditer(_regex_relative_href, haystack)
    for result in results:
        output.append(result.groupdict())
    
    return output
