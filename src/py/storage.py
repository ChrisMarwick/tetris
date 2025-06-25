from abc import ABC, abstractmethod


class BaseStorageAdaptor(ABC):

    @abstractmethod
    def load(self, key):
        pass

    @abstractmethod
    def save(self, key, value):
        pass


class InMemoryStorage(BaseStorageAdaptor):

    def __init__(self, initial_data=None):
        self.data = initial_data or {}

    def load(self, key):
        return self.data.get(key)

    def save(self, key, value):
        self.data[key] = value
