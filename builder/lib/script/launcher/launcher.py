from abc import abstractmethod


class Launcher:

    @abstractmethod
    def generate(self):
        pass


    @abstractmethod
    def _prepare_dirs(self, dir_helper):
        pass


    @abstractmethod
    def _prepare_res(self, res_helper):
        pass


    @abstractmethod
    def _prepare_config(self, config_helper):
        pass


    @abstractmethod
    def _build_app(self):
        pass
