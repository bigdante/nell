from mongoengine import *


class BaseConcept(Document):
    """
    Entity types (concepts) based on Hailong's hierarchy
    """
    # values
    text = StringField(required=True)
    hypernym = ListField(LazyReferenceField('self'))
    hyponym = ListField(LazyReferenceField('self'))

    # allowed relations
    asHeadConstraint = ListField(ReferenceField('BaseRelation'))
    asTailConstraint = ListField(ReferenceField('BaseRelation'))  # not available at the moment

    # source
    source = StringField(required=True)  # not available at the moment
    sourceId = StringField()  # not available at the moment

    meta = {
        "collection": "concept",
        "indexes": [
            "$text"
        ]
    }

