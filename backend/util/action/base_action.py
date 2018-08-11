import json

import time


class BaseAction:

    REDIRECT_ACTION = "redirect"
    CHECK_ACTION = "check"
    ERROR_ACTION = "error"

    SUCCESS_CODE = 0

    BUILD_SUBCODE = 1
    CHECK_CREATED_SUBCODE = 2

    @staticmethod
    def create_action(action: str, code: int, subcode: int, data: dict) -> dict:

        return json.dumps({
            "action": action,
            "code": code,
            "subcode": subcode,
            "data": data,
            "time": time.time()
        })
