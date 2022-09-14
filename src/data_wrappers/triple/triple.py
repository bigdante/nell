from ..entity import MentionEntity
from ..relation import SourceRelation

from datetime import datetime
from typing import Dict


class Triple:
    def __init__(self,
                 _id: str,
                 head: MentionEntity,
                 relation: SourceRelation,
                 tail: MentionEntity,
                 sentence_id: str,
                 extractor: str,
                 timestamp: datetime,
                 **kwargs):
        self.id: str = _id
        self.head: MentionEntity = head
        self.relation: SourceRelation = relation
        self.tail: MentionEntity = tail
        self.sentence_id: str = sentence_id
        self.extractor: str = extractor
        self.timestamp: datetime = timestamp
        self.meta: Dict = kwargs

    def get_cls_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return "[{}: {}; {}; {}]".format(self.get_cls_name(), str(self.head), str(self.relation), str(self.tail))

    def to_dict(self) -> Dict:
        return {
            "head": str(self.head),
            "relation": str(self.relation),
            "tail": str(self.tail),
            "extractor": self.extractor,
            "ts": str(self.timestamp)
        }
