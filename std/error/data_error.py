from std.error.base_error import BaseError


class DataError(BaseError):
    
    # Error codes
    not_found = 1
    data_invalid = 2
    bundle_invalid = 3
    platform_invalid = 3

    theme_not_json = 4

    # Error messages
    not_found_mes = "Data with value {%s} is not founded"
    data_invalid_mes = "Data with value {%s} is invalid"
    version_invalid_mes = "Version number {%s} must be lower than 24 symbols"
    data_invalid_langs = "You need specify one or more language"
    bundle_invalid_mes = "Bundle with name {%s} is invalid"
    theme_json_mes = "Theme with data {%s} is not JSON"
    platform_mess = "Unknown platform"

    def __init__(self, subcode: int=0, data: str="Unknown data error"):
        BaseError.__init__(self, code=BaseError.DATA_CODE, subcode=subcode, data=data)
