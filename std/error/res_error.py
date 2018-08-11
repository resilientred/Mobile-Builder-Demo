
# Error codes
from std.error.base_error import BaseError


class ResourceError(BaseError):

    # Error codes
    res_not_found = 1
    res_exist = 2

    android_image = 3
    android_folder = 4

    ios_image = 5
    ios_folder = 6

    google_res = 7

    file_type = 8

    android_has_excess = 9
    ios_has_excess = 11
    google_has_excess = 10

    # Error message
    res_not_found_mes = "Resource with name {%s} not founded"
    res_exist_mes = "Resource with name {%s} already exist"

    android_image_mes = "Android image {%s} not founded"
    android_folder_mes = "Android folder {%s} not founded"

    ios_image_mes = "iOS image {%s} not founded"
    ios_image_res = "iOS resource not founded"
    ios_folder_mes = "iOS folder {%s} not founded"

    google_res_mes = "Resource have {%s} and it not equal google-services.json"

    file_type_mes = "File with name {%s} must be {%s}"

    android_excess_mes = "Android images resource has excess elements {%s}"
    ios_excess_mes = "iOS images resource has excess elements {%s}"


    def __init__(self, subcode: int=0, data: str="Unknown error with resource"):
        BaseError.__init__(self, code=BaseError.RESOURCE_CODE, subcode=subcode, data=data)
