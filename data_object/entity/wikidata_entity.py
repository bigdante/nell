from .base_entity import *


class WikidataEntity(BaseEntity):
    """
    Wikidata entity (entry)
    """
    # other infromation
    aliases = ListField()

    # source
    source = StringField(default='wikidata')

    # types
    types = DictField()

    meta = {
        "collection": "wikidata_entity"
    }
