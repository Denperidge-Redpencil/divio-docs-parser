# Built-in imports
from typing import Dict

class DivioDocs():
    def __init__(self, tutorials:Dict=dict(), how_to_guides:Dict=dict(), explanation:Dict=dict(), reference:Dict=dict()) -> None:
        self.tutorials = tutorials
        self.how_to_guides = how_to_guides
        self.explanation = explanation
        self.reference = reference

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
        return list(self.get(section_name).values())
    
    def get(self, section_name, file_name: str=None) -> Dict:
        section = getattr(self, section_name)
        if not file_name:
            return section
        else:
            return section[file_name]
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "tutorials": self.tutorials,
            "how_to_guides": self.how_to_guides,
            "explanation": self.explanation,
            "reference": self.reference
        }