from mongoengine import *


class DatasetMention(EmbeddedDocument):
    """
    Class for dataset mentions.
    Using EmbeddedDocument as it is not necessary to create an individual collection.
    """
    # values
    text = StringField(required=True)
    charSpan = ListField(IntField())  # this span should be a relative one
    tokenSpan = ListField(IntField())

    # type (produced by mention detector, e.g. NER tools)
    mentionType = StringField()
    mentionAnnotator = StringField()
    mentionConfidence = FloatField(min_value=0.0, max_value=1.0)

    # temp information
    temp = DictField()
