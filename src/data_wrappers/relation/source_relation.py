from .base_relation import BaseRelation


class SourceRelation(BaseRelation):
    def __init__(self, _id: str, surface: str, source_name: str, source_id: str, **kwargs):
        super(SourceRelation, self).__init__(_id, surface, **kwargs)
        self.source_name: str = source_name
        self.source_id: str = source_id
