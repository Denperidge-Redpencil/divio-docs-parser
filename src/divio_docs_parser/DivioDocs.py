# Built-in imports
from typing import Dict


class DivioDocs():
    def __init__(self, tutorials:Dict=dict(), how_to_guides:Dict=dict(), explanation:Dict=dict(), reference:Dict=dict()) -> None:
        self.tutorials = tutorials
        self.how_to_guides = how_to_guides
        self.explanation = explanation
        self.reference = reference

    def set(self, section_name: str, file_name, content: str):
        self[section_name][file_name] = content
    
    def joined(self, section_name: str):
        return self.tutorials.values()
    
    def get(self, section_name, file_name: str=None):
        #if not file_name:
         #   return
        return self[section_name][file_name]
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "tutorials": self.tutorials,
            "how_to_guides": self.how_to_guides,
            "explanation": self.explanation,
            "reference": self.reference
        }