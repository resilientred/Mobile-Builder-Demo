from abc import abstractmethod


class Disk:

    @abstractmethod
    def upload_file(self, file_name, file_path) -> None:
        pass


    @abstractmethod
    def load_file(self, name: str, path: str, folder_id: str) -> bool:
        pass


    @abstractmethod
    def auth(self) -> None:
        pass


    @abstractmethod
    def check(self, name: str, folder_id: str) -> bool:
        pass


    @abstractmethod
    def delete(self, name: str, folder_id: str) -> None:
        pass


    @abstractmethod
    def replace_file(self, path: str, name: str, folder_id: str) -> None:
        pass


    @abstractmethod
    def create_folder(self, name: str) -> None:
        pass


    @abstractmethod
    def get_folder_id_by_name(self, name: str, folder_id: str) -> str:
        pass


    @abstractmethod
    def check_folder_id_by_name(self, name: str, folder_id: str) -> str:
        pass
