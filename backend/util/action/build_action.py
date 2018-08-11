
from backend.util.action.base_action import BaseAction


class BuildAction(BaseAction):

    BUILD_BASE = 0
    BUILD_CREATED = 1
    BUILD_WAITING = 2
    BUILD_EXECUTING = 3
    BUILD_SUCCESS = 4
    BUILD_ERROR = 5


    @staticmethod
    def create_action_build(action: str, subcode: int, data: dict) -> dict:
        return BaseAction.create_action(action=action, code=BaseAction.BUILD_SUBCODE, subcode=subcode, data=data)


    @staticmethod
    def data_created_build(url) -> dict:
        return {"url": url}
