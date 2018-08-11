from abc import abstractmethod

from builder.lib.model.entity.letter import Letter

YANDEX_MAIL = 'yandex'
GOOGLE_MAIL = 'google'


class Mail:

    @abstractmethod
    def connect(self, *args) -> None:
        pass


    @abstractmethod
    def send_letter(self, letter: Letter) -> None:
        pass


    @abstractmethod
    def disconnect(self) -> None:
        pass
