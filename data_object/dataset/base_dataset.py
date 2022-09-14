from mongoengine import *

from .base_split import BaseSplit


class BaseDataset(Document):
    """
    BaseDataset for handling evaluation/training dataset.
    """
    # values
    name = StringField(required=True)
    task = StringField(required=True)

    numOfSplit = IntField(min_value=1)
    split = MapField(EmbeddedDocumentField(BaseSplit))
    metric = ListField(StringField(), required=True)

    meta = {
        "collection": "dataset"
    }
