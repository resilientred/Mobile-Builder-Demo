from std.error.base_error import BaseError


class DataBaseError(BaseError):
    # Error codes
    duplicate_code = 1


    def __init__(self, subcode: int=0, data: str="Unknown data error"):
        BaseError.__init__(self, code=BaseError.DATA_CODE, subcode=subcode, data=data)
