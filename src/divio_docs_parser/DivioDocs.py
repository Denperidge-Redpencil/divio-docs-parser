# Built-in imports
from typing import Dict
from .md_to_sections import parse_sections_from_markdown
from .Section import Section



class DivioDocs():
    def __init__(self,
                 input_string_or_path: str=None,
                 regex_tutorials =      r"(tutorial|getting\W*started)",
                 regex_how_to_guides =  r"(how\W*to|guide|usage)", 
                 regex_explanation =    r"(explanation|discussion|background\W*material)",
                 regex_reference =      r"(reference|technical)"
            ) -> None:
        """
        input
        """
        
        self.tutorials:     Dict[str, str] = dict()
        self.how_to_guides: Dict[str, str] = dict()
        self.explanation:   Dict[str, str] = dict()
        self.reference:     Dict[str, str] = dict()

        self._tutorials = Section("tutorials", regex_tutorials)
        self._how_to_guides = Section("how_to_guides", regex_how_to_guides)
        self._explanation = Section("explanation", regex_explanation)
        self._reference = Section("reference", regex_reference)
        
        if input_string_or_path:
            self.import_docs(input_string_or_path)
        
        

    def set(self, section_name: str, file_name: str, content: str):
        section: Dict = getattr(self, section_name)
        try:
            section[file_name] = content
        except KeyError:
            print("error")
    
    def _pre_or_append(self, section_name: str, file_name, added_content: str, append=True):
        old_content = self.get(section_name, file_name)
        if append:
            new_content = old_content + added_content
        else:
            new_content = added_content + old_content

        self.set(section_name, file_name, new_content)
    
    def prepend(self, section_name: str, file_name: str, added_content: str):
        self._pre_or_append(section_name, file_name, added_content, append=False)
    
    def append(self, section_name: str, file_name: str, added_content: str):
        self._pre_or_append(section_name, file_name, added_content, append=True)
    
    
    def joined(self, section_name: str) -> list:
        return list(getattr(self, section_name).values())
    
    def get(self, section_name, file_name: str) -> str:
        section = getattr(self, section_name)

        try:
            return section[file_name]
        except KeyError:
            section[file_name] = ""
            return self.get(section_name, file_name)
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "tutorials": self.tutorials,
            "how_to_guides": self.how_to_guides,
            "explanation": self.explanation,
            "reference": self.reference
        }
    
    @property
    def _sections(self):
        return [
            (self.tutorials,        self._tutorials),
            (self.how_to_guides,    self._how_to_guides),
            (self.explanation,      self._explanation),
            (self.reference,        self._reference),
        ]
    
    @property
    def _sectionObjects(self):
        return [self._tutorials, self._how_to_guides, self._explanation, self._reference]
    
    def import_docs(self, filename_or_string: str, section_name=None):
        content = parse_sections_from_markdown(self._sectionObjects, filename_or_string, section_name)

        for section_id in content:
            self.append(section_id, "README.md", content[section_id])
        
        return self
        
