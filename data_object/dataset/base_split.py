from mongoengine import *


class BaseSplit(EmbeddedDocument):
    """
    BaseDataset for handling evaluation/training dataset.
    """
    # values
    name = StringField(required=True)
    keys = ListField(StringField())
    features = DictField()

    train = ListField(GenericReferenceField())
    valid = ListField(GenericReferenceField())
    test = ListField(GenericReferenceField())
    others = MapField(ListField(GenericReferenceField()))

    dataset = ReferenceField('BaseDataset')

    def get_id(self):
        feats = [f"{key}-{self.features[key]}" for key in self.keys]
        feats = [self.dataset.name, self.dataset.task] + feats
        return "_".join(feats)
