from .base_fact import *

from ..mention import BaseMention


class TripleFact(BaseFact):
    """
    Store text-based triple evidence.
    """
    head = StringField(required=True)
    relationLabel = StringField(required=True)
    tail = StringField(required=True)

    headSpan = ListField(IntField(), required=True)
    relation = ReferenceField('BaseRelation', required=True)
    tailSpan = ListField(IntField())

    evidence = GenericReferenceField(required=True)
    # evidence = ReferenceField(required=True)
    evidenceText = StringField()

    verification = DictField()

    meta = {
        "collection": "triple_fact_new",
        "db_alias": "NePtune"
    }
