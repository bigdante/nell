from mongoengine import *


class BaseEntity(Document):
    """
    Base class for all kinds of entities (e.g., wikipedia, wikidata, and other KGs)
    """
    # values
    text = StringField(required=True)
    source = StringField(required=True)
    sourceId = StringField()

    # equivalent entities/pages in other knowledge bases
    equivalents = MapField(GenericReferenceField())
    describedPages = ListField(GenericLazyReferenceField())
    description = StringField()

    # entity types
    types = ListField(ListField(ReferenceField('BaseConcept')))

    meta = {
        "abstract": True,
        # "indexes": [
        #     "source",
        #     "sourceId"
        # ]
    }
