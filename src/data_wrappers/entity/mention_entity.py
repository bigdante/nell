from .source_entity import SourceConcept, SourceEntity

from typing import List, Union
from interval3 import Interval
from bson import ObjectId


class MentionEntity(SourceEntity):
    def __init__(self,
                 _id: str,
                 surface: str,
                 types: Union[List[SourceConcept], None],
                 sentence_id: str,
                 doc_id: str,
                 char_span: Union[List[int], Interval],
                 extractor: str,
                 aligned_sid: Union[str, None] = None,
                 **kwargs):
        super(MentionEntity, self).__init__(_id, surface, types,
                                            source_name=None,
                                            source_id=None,
                                            aligned_uid=None,
                                            **kwargs)
        self.sentence_id: str = sentence_id
        self.doc_id: str = doc_id
        self.char_span: Interval
        if type(char_span) is Interval:
            self.char_span = char_span
        else:
            self.char_span = Interval(lower_bound=char_span[0], upper_bound=char_span[1], lower_closed=True,
                                      upper_closed=False)
        self.extractor: str = extractor
        self.aligned_sid: Union[str, None] = aligned_sid

    def get_span(self):
        return self.char_span.lower_bound, self.char_span.upper_bound

    def has_source(self):
        return self.aligned_sid is not None

    def has_types(self):
        return self.types is not None

    @classmethod
    def from_source(cls, src_ent: SourceEntity, sentence_id: str, doc_id: str, char_span: Union[List[int], Interval],
                    extractor: str):
        mnd_ent = cls(_id=str(ObjectId()),
                      surface=src_ent.surface,
                      types=src_ent.types,
                      sentence_id=sentence_id,
                      doc_id=doc_id,
                      char_span=char_span,
                      extractor=extractor,
                      aligned_sid=src_ent.id)
        mnd_ent.source_name = src_ent.source_name
        mnd_ent.source_id = src_ent.source_id
        mnd_ent.aligned_uid = src_ent.aligned_uid

        return mnd_ent
