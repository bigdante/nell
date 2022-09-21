from typing import List, Dict, Union
from abc import abstractmethod

from ..concept import SourceConcept


class BaseEntity:
    def __init__(self,
                 _id: str,
                 surface: str,
                 types: Union[List[SourceConcept], None],
                 **kwargs):
        self.id: str = _id
        self.surface: str = surface
        self.types: List[SourceConcept] = types
        self.meta: Dict = kwargs

    def get_cls_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return "[{}: {}]".format(self.get_cls_name(), self.surface)

    # @abstractmethod
    # def to_dict(self) -> Dict:
    #     pass
