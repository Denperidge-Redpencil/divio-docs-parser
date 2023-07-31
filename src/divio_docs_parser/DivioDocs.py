# Built-in imports
from os.path import isdir
from typing import Dict

# Local imports
from .utils.markdown_parser import parse_sections_from_markdown
from .utils.files import list_all_markdown_files
from .Section import Section
from .constants import *



class DivioDocs():
    """The class used to collect & parse divio style documentation from a directory/project/repo"""

    def __init__(self,
                 input_string_or_path: str=None,
                 regex_tutorials =      r"(tutorial|getting\W*started)",
                 regex_how_to_guides =  r"(how\W*to|guide|usage)", 
                 regex_explanation =    r"(explanation|discussion|background\W*material)",
                 regex_reference =      r"(reference|technical)"
            ) -> None:
        """
        `input_string_or_path`: (Optional) Filename or string to collect & parse. More can be collected later
        
        `regex_{SECTION}`: (Optional) The regex that will be used to parse the SECTION's contents
        """
        
        self.tutorials:     Dict[str, str] = dict()
        """Dictionary containing the collected `tutorials` in a { `filename`: `content` } structure"""
        self.how_to_guides: Dict[str, str] = dict()
        """Dictionary containing the collected `how-to guides` in a { `filename`: `content` } structure"""
        self.explanation:   Dict[str, str] = dict()
        """Dictionary containing the collected `explanation` in a { `filename`: `content` } structure"""
        self.reference:     Dict[str, str] = dict()
        """Dictionary containing the collected `reference` in a { `filename`: `content` } structure"""

        self._tutorials = Section(ID_TUTORIALS, regex_tutorials)
        self._how_to_guides = Section(ID_HOW_TO_GUIDES, regex_how_to_guides)
        self._explanation = Section(ID_EXPLANATION, regex_explanation)
        self._reference = Section(ID_REFERENCE, regex_reference)
        
        if input_string_or_path:
            self.import_docs(input_string_or_path)
        

    def _set(self, section_name: str, file_name: str, content: str):
        """Set self.SECTION_NAME.FILENAME to CONTENT"""
        section: Dict = getattr(self, section_name)
        try:
            section[file_name] = content
        except KeyError:
            print("error")
    
    def _pre_or_append(self, section_name: str, file_name, added_content: str, append=True):
        """Wraps the set function, but without replacing the contents: instead prepending or appending"""
        old_content = self._get(section_name, file_name)
        if append:
            new_content = old_content + added_content
        else:
            new_content = added_content + old_content

        self._set(section_name, file_name, new_content)
    
    def _prepend(self, section_name: str, file_name: str, added_content: str):
        """Prepends content to the specified filename in the section"""
        self._pre_or_append(section_name, file_name, added_content, append=False)
    
    def _append(self, section_name: str, file_name: str, added_content: str):
        """Appends content to the specified filename in the section"""
        self._pre_or_append(section_name, file_name, added_content, append=True)
    
    
    def section_without_filenames(self, section_name: str) -> list:
        """Returns the section as a list, with the filenames omitted"""
        return list(getattr(self, section_name).values())
    
    def _get(self, section_name, file_name: str) -> str:
        """Gets the sections file, creating an empty value for it if none can be found"""
        section = getattr(self, section_name)

        try:
            return section[file_name]
        except KeyError:
            section[file_name] = ""
            return self._get(section_name, file_name)
    
    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """Returns all the collected docs in a { `section_name`: { `filename`: `content` } } format"""
        return {
            ID_TUTORIALS: self.tutorials,
            ID_HOW_TO_GUIDES: self.how_to_guides,
            ID_EXPLANATION: self.explanation,
            ID_REFERENCE: self.reference
        }
    
    @property
    def _sections(self):
        """
        Returns a list in the following format: ({SECTION_DICT}, {SECTION_CLASS_OBJECT})
        in the order of tutorials, how-to guides, explanation and reference
        """
        return [
            (self.tutorials,        self._tutorials),
            (self.how_to_guides,    self._how_to_guides),
            (self.explanation,      self._explanation),
            (self.reference,        self._reference),
        ]
    
    @property
    def _sectionObjects(self):
        """Returns every Section object in a list: [`_tutorials`, `_how_to_guides`, `_explanation`, `_reference`]"""
        return [self._tutorials, self._how_to_guides, self._explanation, self._reference]
    
    def _import_doc(self, path_or_string, filename: str=None):
        content = parse_sections_from_markdown(self._sectionObjects, path_or_string, filename)

        for section_id in content:
            self._append(section_id, "README.md", content[section_id])
        
        return self
    
    def import_docs(self, path_or_string: str):
        """
        Collects & parses all documentation within either the file at the path provided, or the string provided
        
        Optionally set `section_id` to override the automatic section detection and add the contents to the specified section 
        """

        if not isdir(path_or_string):
            self._import_doc(path_or_string)
        else:
            all_md_files = list_all_markdown_files(path_or_string)
            for md_file in all_md_files:
                self._import_doc(md_file)

        return self
