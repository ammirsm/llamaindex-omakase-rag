__all__ = ["BaseSyncer", "BaseLoader", "BaseBuilder"]

import abc


class BaseSyncer(abc.ABC):
    @abc.abstractmethod
    def sync(self, data):
        pass


class BaseLoader(abc.ABC):
    @abc.abstractmethod
    def load_data(self):
        pass


class BaseBuilder(abc.ABC):
    @abc.abstractmethod
    def build(self):
        pass
