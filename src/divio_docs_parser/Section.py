from re import RegexFlag, sub, escape
from typing import Union, Match
from .Args import args
from .utils.regex import search_ignorecase_multiline, search_ignorecase_multiline_dotallnewline

"""Defines section (how_to_guides, tutorials...) classes"""

class Section:
    """Class to represent a Section"""
    def __init__(self, name: str, regex:r"str") -> None:
        self.name = name
        self.regex = regex
    
    @property
    def regex_with_md_header(self):
        """Returns the regex to find this section, accounting for Markdown headers"""
        return r"^#.*" + self.regex
    

    def _header_from(self, haystack: str) -> Union[str, None]:
        """Returns the contents of this section from a string"""
        try:
            return search_ignorecase_multiline(self.regex_with_md_header, haystack).group()
        except AttributeError:
            return None
    
    def header_in(self, haystack: str) -> bool:
        """Returns True if this section can be found in a string"""
        return bool(self._header_from(haystack))
    

    def _header_tags_from(self, input_string: str):
        """
        Get the markdown header tags from this header, with whitespace

        Example with tutorials:
        Input:
        ## Docs
        ...
        ### Tutorials
        ...

        Output: `### `
        """
        result = search_ignorecase_multiline(r"#*\W", self._header_from(input_string))

        return result.group() if result else None
    
    def _content_from(self, input_string: str):
        """Find and return everything between the section header and the header of the next section"""
        # Okay, extracting the content will be a bit complex
        # The regex will contain 3 parts/groups
        # Group 1: the header of the section 
        #print(self._header_from(input_string))
        regex = r"(^" + escape(self._header_from(input_string)) + ")" # Start of line, header, end of line
        regex += "(.*)" # All content in between the section header and...
        regex += escape(self._header_tags_from(input_string)) + "(\s|\w)"  # The next header of the same size
        try:
            return search_ignorecase_multiline_dotallnewline(regex, input_string).groups()[1]  # Use the S flag
        except AttributeError:
            # If the regex fails, its possible there is no following header
            # TODO cleaner solution
            regex = r"(^" + escape(self._header_from(input_string)) + ")" # Start of line, header, end of line
            regex += "(.*)" # All content in between the section header and...
            return search_ignorecase_multiline_dotallnewline(regex, input_string).groups()[1]  # Use the S flag
    
    def parse_from(self, input_string: str) -> str:
        """Extracts and parses the section header & content from a string, returning a new string with corrected header tags"""
        # Now we have the unparsed section content,
        # but the headers are all still based on the old file. And our header isn't there!

        # To guide you through this, we'll use an example with the following structure
        # ### Tutorials
        # #### First one
        # ##### Subthing
        # #### Second one

        #print(self.sourceContent)
        #print(self.section.name)
        originalBaseHeaderlevel = self._header_tags_from(input_string).count('#')  # Example output: 3
        lowerEveryHeaderlevelBy = originalBaseHeaderlevel - 1  # Example output: 2

        output = self._header_from(input_string) + self._content_from(input_string)  # Add the original header


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

        
    

"""Section definitions. This is where you can customise synonyms"""
sections = {
    "tutorials": Section(args.tutorials,       r"(tutorial|getting\W*started)"),
    "how_to_guides": Section(args.how_to_guides,             r"(how\W*to|guide|usage)"),
    "explanation": Section(args.explanation, r"(explanation|discussion|background\W*material)"),
    "reference": Section(args.reference,     r"(reference|technical)")
}




