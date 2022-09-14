from mongoengine import *


class BaseFact(Document):
    """
    Base class for facts, including KB-style, event-style and potentially others.
    """
    # values TODO: create classes for annotators
    annotator = ListField(StringField())
    numOfAnnotators = IntField()

    meta = {
        "abstract": True
    }
