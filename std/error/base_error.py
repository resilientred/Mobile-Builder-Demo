import json

import time


class BaseError(Exception):

    # Response Messages
    BASE_DATA = "Unknown error with resource"

    # Response Codes
    BASE_CODE = 0
    PATH_CODE = 1
    DATA_CODE = 2
    RESOURCE_CODE = 3
    BUILD_CODE = 4
    DATA_BASE_CODE = 5

    # Response Info
    BASE_INFO = "Unknown error"
    ACTION_ERROR = "error"


    def __init__(self, code: int=BASE_CODE, subcode: int=BASE_CODE, data: str=BASE_DATA):
        self.code = code
        self.subcode = subcode
        self.data = data


    def generate_error(self) -> str:
        return json.dumps({
            "action": self.ACTION_ERROR,
            "code": self.code,
            "subcode": self.subcode,
            "data": {
                "message": self.data
            },
            "time": time.time()
        })


    @staticmethod
    def generate_base_error(data: str = BASE_DATA) -> str:
        return json.dumps({
            "action": BaseError.ACTION_ERROR,
            "code": BaseError.BASE_CODE,
            "subcode": BaseError.BASE_CODE,
            "data": {
                "message": data
            },
            "time": time.time()
        })
