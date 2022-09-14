from .base_page import *
from mongoengine import *

class WikipediaPage(BasePage):
    """
    Wikipedia pages
    """
    # source
    source = StringField(default="wikipedia")
    source_id = StringField(required=True)
    meta = {
        # "abstract": True,
        "collection": "page",
        # "indexes": [
        #     "source_id",
        #     "source"
        # ]
        "db_alias": "NePtune"
    }
