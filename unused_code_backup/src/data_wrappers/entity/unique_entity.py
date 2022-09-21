from .base_entity import BaseEntity, SourceConcept

from typing import List, Union


class UniqueEntity(BaseEntity):
    def __init__(self,
                 _id: str,
                 surface: str,
                 types: Union[List[SourceConcept], None],
                 aligned_sids: List[str],
                 **kwargs):
        super(UniqueEntity, self).__init__(_id, surface, types, **kwargs)
        self.aligned_sids: List[str] = aligned_sids
