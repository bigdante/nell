from mongoengine import *


class DatasetFact(EmbeddedDocument):
    """
    Store text-based triple evidence.
    """
    head = StringField(required=True)
    relationLabel = StringField(required=True)
    tail = StringField(required=True)

    headMentionId = IntField(required=True)
    relation = GenericReferenceField()
    tailMentionId = IntField(required=True)
