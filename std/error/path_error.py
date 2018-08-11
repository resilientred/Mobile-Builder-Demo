from std.error.base_error import BaseError


class PathError(BaseError):
    # Error codes
    path_not_found = 1
    path_exist = 1

    # Error messages
    path_not_found_mes = "Path with name {%s} is not founded"
    path_exist_mes = "Path with name {%s} already exist"


    def __init__(self, subcode: int=0, data: str="Unknown path error"):
        BaseError.__init__(self, code=BaseError.PATH_CODE, subcode=subcode, data=data)
