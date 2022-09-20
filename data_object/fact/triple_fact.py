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
    is_from_abstract = StringField(required=True)
    headWikidataEntity = StringField(required=True)
    headWikipediaEntity = StringField(required=True)

    meta = {
        # "collection": "triple_fact_new",
        "collection": "triple_fact_v0_1_20220919",
        "db_alias": "NePtune"
    }
