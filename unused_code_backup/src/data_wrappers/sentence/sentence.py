from typing import Dict, List, Union
from interval3 import Interval

from ..entity import MentionEntity


class Sentence:
    def __init__(self,
                 _id: str,
                 text: str,
                 entities: List[MentionEntity],
                 triples: List[str],
                 doc_id: str,
                 index: int,
                 char_span: Union[List[int], Interval],
                 source_name: str,
                 **kwargs):
        self.id: str = _id
        self.text: str = text
        self.entities: List[MentionEntity] = entities
        self.triples: List[str] = triples
        self.doc_id: str = doc_id
        self.index: int = index
        self.char_span: Interval
        if type(char_span) is Interval:
            self.char_span = char_span
        else:
            self.char_span = Interval(lower_bound=char_span[0], upper_bound=char_span[1], lower_closed=True,
                                      upper_closed=False)
        self.source_name: str = source_name
        self.meta: Dict = kwargs

    def get_span(self):
        return self.char_span.lower_bound, self.char_span.upper_bound
