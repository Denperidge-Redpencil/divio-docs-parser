from re import search, RegexFlag, sub, escape
from config import section_names

def regex(needle: r"str", haystack: str, flags):
    return search(needle, haystack, flags)

def regexIM(needle: r"str", haystack: str):
    return regex(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE)
    
# Includes https://docs.python.org/3/library/re.html#re.S
def regexIMS(needle: r"str", haystack: str):
    return regex(needle, haystack, RegexFlag.IGNORECASE | RegexFlag.MULTILINE | RegexFlag.S)

class Section:
    def __init__(self, name: str, headertext: str, regex:r"str") -> None:
        self.name = name
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
        self.sourceContent = str()
    
    @property
    def header(self):
        return self.section.find_in(self.sourceContent, header=True).group()

    @property
    def headertags(self):
        # Example output: ###
        try:
            return regexIM(r"#*\W", self.header).group()
        except AttributeError:
            #print(self.section.name)
            return None
    
    # This will return everything between 
    @property
    def sectionContent(self):
        # Okay, extracting the content will be a bit complex
        # The regex will contain 3 parts/groups
        # Group 1: the header of the section 
        regex = r"(^" + escape(self.header) + ")" # Start of line, header, end of line
        regex += "(.*)" # All content in between the section header and...
        regex += escape(self.headertags) + "(\s|\w)"  # The next header of the same size
        try:
            return regexIMS(regex, self.sourceContent).groups()[1]  # Use the S flag
        except AttributeError:
            # If the regex fails, its possible there is no following header
            # TODO cleaner solution
            regex = r"(^" + escape(self.header) + ")" # Start of line, header, end of line
            regex += "(.*)" # All content in between the section header and...
            return regexIMS(regex, self.sourceContent).groups()[1]  # Use the S flag
    
    @property
    def output(self):
        # Now we have the unparsed section content,
        # but the headers are all still based on the old file. And our header isn't there!

        # To guide you through this, we'll use an example with the following structure
        # ### Tutorials
        # #### First one
        # ##### Subthing
        # #### Second one

        #print(self.sourceContent)
        #print(self.section.name)
        originalBaseHeaderlevel = self.headertags.count('#')  # Example output: 3
        lowerEveryHeaderlevelBy = originalBaseHeaderlevel - 1  # Example output: 2

        output = self.header + self.sectionContent  # Add the original header


        header_regex = r"^#*"
        
        def lower_header(match):
            string = match.group()  # Example: ###
            originalHeaderlevel = string.count("#")  # Example: 3
            if originalHeaderlevel > 0:
                newHeaderLevel = originalHeaderlevel - lowerEveryHeaderlevelBy  # Example: 2
                string = sub(header_regex, "#"*newHeaderLevel, string)  # Example: #
            return string
            
        # run lower_header on every header in here
        output = sub(header_regex, lower_header, output, flags=RegexFlag.IGNORECASE|RegexFlag.MULTILINE)        

        return output

        
        
    


sections = {
    "tutorials": Section(section_names["tutorials"], " tutorials ", r"(tutorial|getting\W*started)"),
    "howtos": Section(section_names["how-tos"], "how to's", r"(how\W*to|guide|usage)"),
    "explanations": Section(section_names["explanations"], "explanation(s)", r"(explanation|discussion|background\W*material)"),
    "references": Section(section_names["references"], "reference(s)", r"(reference|technical)")
}




