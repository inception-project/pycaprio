from abc import ABCMeta
from abc import abstractmethod
from typing import Generic
from typing import List
from typing import Literal
from typing import TypeVar
from typing import Union
from typing import overload

T = TypeVar("T")

serialized_type = Union[List[dict], dict]


class BaseInceptionSchema(Generic[T], metaclass=ABCMeta):
    @overload
    def load(self, serialized_object_or_list: List[dict], many: Literal[True]) -> List[T]: ...

    @overload
    def load(self, serialized_object_or_list: dict, many: Literal[False] = False) -> T: ...

    @abstractmethod
    def load(self, serialized_object_or_list: serialized_type, many: bool = False) -> Union[List[T], T]:
        """
        Deserializes object from a dictionary.
        :param serialized_object_or_list: Dictionary/List containing the serialized object.
        :param many: Whether object is list or dictionary. Defaults to False (single object).
        :return: Deserialized object.
        """
        pass  # pragma: no cover

    @overload
    def dump(self, deserialized_object_or_list: List[T], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, deserialized_object_or_list: T, many: Literal[False] = False) -> dict: ...

    @abstractmethod
    def dump(self, deserialized_object_or_list: Union[List[T], T], many: bool = False) -> serialized_type:
        """
        Serializes object into a dictionary
        :param deserialized_object_or_list: Object/List of objects to be serialized.
        :param many: Whether object is a list or not. Defaults to False (single object)
        :return: Serialized object.
        """
        pass  # pragma: no cover
