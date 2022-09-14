from .base_entity import *


class WikipediaEntity(BaseEntity):
    """
    Wikipedia entity (entry)
    """
    # source
    source = StringField(default='wikipedia')

    # url
    url = URLField()

    meta = {
        "collection": "entity"
    }
