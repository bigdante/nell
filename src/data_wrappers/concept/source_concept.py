from .base_concept import BaseConcept

from typing import List, Dict


class SourceConcept(BaseConcept):
    def __init__(self, _id: str, surface: str, hypernyms: List[str], source_name: str, source_id: str, **kwargs):
        super(SourceConcept, self).__init__(_id, surface, hypernyms, **kwargs)
        self.source_name: str = source_name
        self.source_id: str = source_id
