from abc import ABC, abstractmethod
# from dotenv import load_dotenv


class BaseStorageAdaptor(ABC):
    """
    Base class for storage, all the client code needs to know is that it's a key value store, data can be saved against
    a key or loaded from the key.
    """

    @abstractmethod
    def load(self, key):
        pass

    @abstractmethod
    def save(self, key, value):
        pass


class InMemoryStorage(BaseStorageAdaptor):
    """
    Simple dictionary implementation of the storage adaptor, useful for unit testing.
    """

    def __init__(self, initial_data=None):
        self.data = initial_data or {}

    def load(self, key):
        return self.data.get(key)

    def save(self, key, value):
        self.data[key] = value
