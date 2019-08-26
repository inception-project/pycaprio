from abc import ABCMeta
from abc import abstractmethod


class BaseInceptionSchema(metaclass=ABCMeta):

    @abstractmethod
    def load(self, serialized_object_or_list, many: bool = False):
        """
        Deserializes object from a dictionary.
        :param serialized_object_or_list: Dictionary/List containing the serialized object.
        :param many: Whether object is list or dictionary. Defaults to False (single object).
        :return: Deserialized object.
        """
        pass  # pragma: no cover

    @abstractmethod
    def dump(self, deserialized_object_or_list, many: bool = False):
        """
        Serializes object into a dictionary
        :param deserialized_object_or_list: Object/List of objects to be serialized.
        :param many: Whether object is a list or not. Defaults to False (single object)
        :return: Serialized object.
        """
        pass  # pragma: no cover
