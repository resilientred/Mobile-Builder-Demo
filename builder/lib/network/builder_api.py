import time

from std.network import api
import requests

from std.std import merge


class MobileApi:

    @staticmethod
    def post_build_status(base_url: str, app_index: int, status: int) -> None:
        data = {
            "app_index": app_index,
            "status": status,
            "time": time.time()
        }

        requests.post(url=merge(base_url + api.post_update_build_status), data=data)


    @staticmethod
    def post_app_build(base_url: str, data: dict) -> None:
        requests.post(url=merge(base_url + api.post_app_build), form=data)
