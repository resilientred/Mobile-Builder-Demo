from abc import abstractmethod


class Consumer:

    @abstractmethod
    def run(self) -> None:
        pass


    @abstractmethod
    def configure(self, *args) -> None:
        pass


    @abstractmethod
    def connect(self) -> None:
        pass


    @abstractmethod
    def __execute(self, *args) -> None:
        pass


    @abstractmethod
    def __empty_execute(self, *args) -> None:
        pass


    @abstractmethod
    def stop(self) -> None:
        pass


    @abstractmethod
    def disconnect(self) -> None:
        pass
