from ..sentence import Sentence

from typing import List, Dict


class Document:
    def __init__(self, _id: str, sentences: List[Sentence], **kwargs):
        self.id: str = _id
        self.sentences: List[Sentence] = sentences
        self.meta: Dict = kwargs
