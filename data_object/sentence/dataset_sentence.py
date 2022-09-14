from mongoengine import *

from ..mention import DatasetMention
from ..fact import DatasetFact


class DatasetSentence(Document):
    """
    Sentence class for sentences in a typical dataset
    """
    # values

    text = StringField(required=True)
    charSpan = ListField(IntField())

    tokens = ListField(StringField())
    mentions = EmbeddedDocumentListField(DatasetMention, required=True)
    facts = EmbeddedDocumentListField(DatasetFact, required=True)
    inParaId = IntField(min_value=0)

    identifier = StringField(required=True)
    temp = DictField()

    meta = {
        "collection": "dataset_sentence"
    }
