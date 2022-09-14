from mongoengine import *


class BaseParagraph(Document):
    """
    Base class for paragraphs, which consists of sentences.
    Not an abstract class (as abstraction seems unnecessary).
    """
    # values
    sentences = ListField(ReferenceField('BaseSentence'))
    charSpan = ListField(IntField())
    inPageId = IntField(min_value=0)

    # reference to upper-level objects
    # refPage = LazyReferenceField("BasePage")

    meta = {
        "collection": "paragraph",
        "db_alias": "NePtune"
    }

    def __getattr__(self, item):
        if item == 'text':
            return self.get_text()
        raise AttributeError(f"Attribute `{item}` not found in object BaseParagraph.")

    def get_text(self):
        text = ''
        for sent_obj in self.sentences:
            text += (" " * (sent_obj.charSpan[0] - self.charSpan[0] - len(text)) + sent_obj.text)
        text += " " * (self.charSpan[1] - self.charSpan[0] - len(text))
        return text
