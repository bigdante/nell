from .base_mention import *

from typing import List


class CorefMention(BaseMention):
    """
    Mentions created by coreference.
    """

    refSpan = ListField(IntField())
    refSent = LazyReferenceField('BaseSentence')

    @classmethod
    def create_coref(cls, base_mention: BaseMention, sentence, text: str, span: List[int]):
        return cls(text=text, charSpan=span,
                   refSpan=base_mention.charSpan,
                   refSent=sentence,
                   entity=base_mention.entity,
                   entityAnnotator=base_mention.entityAnnotator,
                   mentionType=base_mention.mentionType,
                   mentionAnnotator="longformer-coref-joint")
