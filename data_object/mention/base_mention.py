from mongoengine import *

from typing import List


class BaseMention(EmbeddedDocument):
    """
    Base class for mentions.
    Using EmbeddedDocument as it is not necessary to create an individual collection.
    """
    # values
    text = StringField(required=True)
    charSpan = ListField(IntField(), required=True)  # this span should be a relative one

    # linked entity
    entity = ReferenceField('WikipediaEntity')
    entityAnnotator = StringField()
    confidence = FloatField(min_value=0.0, max_value=1.0)

    # type (produced by mention detector, e.g. NER tools)
    mentionType = StringField()
    mentionAnnotator = StringField()
    mentionConfidence = FloatField(min_value=0.0, max_value=1.0)

    # temp information
    temp = DictField()

    meta = {
        "allow_inheritance": True
    }

    @classmethod
    def create_coref(cls, base_mention, text: str, span: List[int]):
        return cls(text=text, charSpan=span,
                   temp={"coref": {
                       "refSpan": base_mention.charSpan,
                       "refSent": base_mention.temp['sentenceId']
                   }},
                   entity=base_mention.entity,
                   entityAnnotator=base_mention.entityAnnotator,
                   mentionType=base_mention.mentionType,
                   mentionAnnotator="longformer-coref-joint")
