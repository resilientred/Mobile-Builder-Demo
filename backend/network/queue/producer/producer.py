from abc import abstractmethod


class Producer:

    @abstractmethod
    def connect(self, *args):
        pass


    @abstractmethod
    def configure(self, *args):
        pass


    @abstractmethod
    def __callback(self):
        pass


    @abstractmethod
    def send(self, message: str, *args):
        pass


    @abstractmethod
    def disconnect(self):
        pass
