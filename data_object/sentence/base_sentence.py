from mongoengine import *

from ..mention import BaseMention


class BaseSentence(Document):
    """
    Base class for sentence, which consists of sentences.
    Not an abstract class (as abstraction seems unnecessary).
    """
    # values
    text = StringField(required=True)
    charSpan = ListField(IntField(), required=True)
    mentions = EmbeddedDocumentListField(BaseMention)
    inParaId = IntField(min_value=0)

    # reference to upper-level objects
    # refPara = LazyReferenceField('BaseParagraph')
    # refPage = LazyReferenceField('BasePage')

    meta = {
        "collection": "sentence",
        "db_alias": "NePtune"
    }
