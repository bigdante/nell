from .unique_entity import BaseEntity, SourceConcept, UniqueEntity

from typing import List, Union


class SourceEntity(BaseEntity):
    def __init__(self, _id: str,
                 surface: str,
                 types: Union[List[SourceConcept], None],
                 source_name: Union[str, None],
                 source_id: Union[str, None],
                 aligned_uid: Union[str, None],
                 **kwargs):
        super(BaseEntity, self).__init__(_id, surface, types, **kwargs)
        self.source_name: Union[str, None] = source_name
        self.source_id: Union[str, None] = source_id
        self.aligned_uid: Union[str, None] = aligned_uid
