from mongoengine import *


class BasePage(Document):
    """
    Base class for pages (articles), including Wikipedia, web pages, news and so on.
    """
    # values
    paragraphs = ListField(ReferenceField('BaseParagraph'), required=True)
    url = URLField()
    pubTime = DateTimeField()

    description = StringField()

    # source
    source = StringField(required=True)
    source_id = StringField()

    meta = {
        "abstract": True,
        "collection": "page",
        # "indexes": [
        #     "source_id",
        #     "source"
        # ],
        "db_alias": "NePtune"
    }
