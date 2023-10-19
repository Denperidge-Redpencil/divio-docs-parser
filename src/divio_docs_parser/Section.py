# Built-in imports
from re import RegexFlag, sub, escape
from typing import Union, Match

# Local imports
from .utils.regex import search_ignorecase_multiline, search_ignorecase_multiline_dotallnewline, grab_relative_hrefs




class Section:
    """
    Defines a section from the Divio documentation structure
    (e.g. tutorials, how-to guides, reference and explanation)

    This class contains everything needed to find and parse section
    content out of a markdown string
    """
    def __init__(self, id: str, regex:r"str") -> None:
        self.id = id
        """Used mostly by markdown_parser to structure output (e.g. {`section_id`: `content`})"""
        self.regex = regex
        """The regex to match (the title of) the section"""

    
    @property
    def regex_with_md_header(self):
        """Returns the regex to find this section, accounting for Markdown headers"""
        return r"^#.*" + self.regex
    

    def _header_from(self, haystack: str, must_have_header_tags=True) -> Union[str, None]:
        """Uses regex_with_md_header to find and return the header in the file, if possible"""
        needle = self.regex_with_md_header if must_have_header_tags else self.regex
        try:
            return search_ignorecase_multiline(needle, haystack).group()
        except AttributeError:
            return None
    
    def header_in(self, haystack: str, must_have_header_tags=True) -> bool:
        """Returns True if the section header is present in the string"""
        return bool(self._header_from(haystack, must_have_header_tags))
    

    def _header_tags_from(self, input_string: str):
        """
        Get the markdown header tags from this header
        (with whitespace included) 

        Example with tutorials:

        Input:
        ```
            ## Docs
            ...
            ### Tutorials
            ...
        ```
        Output: `"### "`
        """
        result = search_ignorecase_multiline(r"#*\W", self._header_from(input_string))

        return result.group() if result else None
    
    def _content_from(self, input_string: str):
        """Find and return everything between the section header and the header of the next section"""
        # Okay, extracting the content will be a bit complex
        # The regex will contain 3 parts/groups

        # Group 1: the header of the section 
        regex = r"(^" + escape(self._header_from(input_string)) + ")" # Start of line, header, end of line
        # Group 2: All content in between the section header and...
        regex += "(.*?)"
        # Group 3: The next header of the same size
        regex += "(?=^" + escape(self._header_tags_from(input_string).strip()) + "[^#])"
        try:
            return search_ignorecase_multiline_dotallnewline(regex, input_string).groups()[1]  # Use the S flag
        except AttributeError:
            # If the regex fails, its possible there is no following header
            # TODO cleaner solution
            regex = r"(^" + escape(self._header_from(input_string)) + ")" # Start of line, header, end of line
            regex += "(.*)" # All content in between the section header and...
            return search_ignorecase_multiline_dotallnewline(regex, input_string).groups()[1]  # Use the S flag
    
    def parse_from(self, input_string: str, import_whole_file=False) -> str:
        """
        Extracts and parses the section header & content from a string,
        returning a new string with corrected header tags
        """
        if import_whole_file:
            return input_string

        # Now we have the unparsed section content,
        # but the headers are all still based on the old file. And our header isn't there!

        # To guide you through this, we'll use an example with the following structure
        # ### Tutorials
        # #### First one
        # ##### Subthing
        # #### Second one


        original_base_header_count = self._header_tags_from(input_string).count('#')  # Example output: 3
        lower_header_count_by = original_base_header_count - 1  # Example output: 2

        output = self._header_from(input_string) + self._content_from(input_string)  # Add the original header

        header_regex = r"^#*"
        
        def lower_header(match):
            string = match.group()  # Example: ###
            originalHeaderlevel = string.count("#")  # Example: 3
            if originalHeaderlevel > 0:
                newHeaderLevel = originalHeaderlevel - lower_header_count_by  # Example: 2
                string = sub(header_regex, "#"*newHeaderLevel, string)  # Example: #
            return string
            
        # run lower_header on every header in here
        output = sub(header_regex, lower_header, output, flags=RegexFlag.IGNORECASE|RegexFlag.MULTILINE)        

        return output

