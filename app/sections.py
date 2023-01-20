from re import search, RegexFlag

class Section:
    def __init__(self, headertext: str, regex:r"str") -> None:
        self.headertext = headertext
        self.regex = regex
    
    @property
    def regexMdHeader(self):
        return r"^#.*" + self.regex
    
    def found_in(self, haystack: str, header = False) -> bool:
        needle = self.regex if not header else self.regexMdHeader

        return bool(search(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE))


sections = {
    "tutorials": Section(" tutorials ", r"tutorial"),
    "howtos": Section("how to's", r"how\W*to"),
    "explanations": Section("explanation(s)", r"reference"),
    "references": Section("reference(s)", r"(explanation|discussion|background\W*material)")
}




