from re import search, RegexFlag

def regex(needle: r"str", haystack: str, flags):
    return search(needle, haystack, flags)

def regexIM(needle: r"str", haystack: str):
    return regex(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    
# Includes https://docs.python.org/3/library/re.html#re.S
def regexIMS(needle: r"str", haystack: str):
    return regex(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE | RegexFlag.S)

class Section:
    def __init__(self, headertext: str, regex:r"str") -> None:
        self.headertext = headertext
        self.regex = regex
    
    @property
    def regexMdHeader(self):
        return r"^#.*" + self.regex
    

    def find_in(self, haystack: str, header = False):
        needle = self.regex if not header else self.regexMdHeader
        return regexIM(needle, haystack)
    
    def found_in(self, haystack: str, header = False) -> bool:
        return bool(self.find_in(haystack, header))


class RepoSection:
    def __init__(self, section: Section) -> None:
        self.section = section
        self.headerlevel = str()
        self.sourceContent = str()
    
    @property
    def header(self):
         return self.section.find_in(self.sourceContent, header=True).group()

    @property
    def headertags(self):
        # Example output: ###
        return regexIM(r"#*\W", self.header).group()
    
    @property
    def sectionContent(self):
        # Okay, extracting the content will be a bit complex
        # The regex will contain 3 parts/groups
        # Group 1: the header of the section 
        regex = r"(^" + self.header + ")" # Start of line, header
        regex += "(.*)" # All content in between the section header and...
        regex += self.headertags + "(\s|\w)"  # The next header of the same size
        return regexIMS(regex, self.sourceContent).groups()[1]  # Use the S flag
        
    


sections = {
    "tutorials": Section(" tutorials ", r"tutorial"),
    "howtos": Section("how to's", r"how\W*to"),
    "explanations": Section("explanation(s)", r"reference"),
    "references": Section("reference(s)", r"(explanation|discussion|background\W*material)")
}




