from mongoengine import *


class BaseRelation(Document):
    """
    data object for relations in KGs; only refers to wikidata properties now.
    """
    # values
    text = StringField(required=True)
    description = StringField()
    alias = ListField(StringField())

    # source
    source = StringField(required=True)
    sourceId = StringField()

    # constraints
    HeadConstraint = MapField(ListField(StringField()))
    TailConstraint = MapField(ListField(StringField()))

    meta = {
        "collection": "relation",
        # "indexes": [
        #     "sourceId",
        #     "$text"
        # ],
        "db_alias": "NePtune"
    }
