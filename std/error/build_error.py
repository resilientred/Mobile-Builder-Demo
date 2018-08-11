

class BuildError(Exception):

    # Error codes
    path_error = 1
    country_error = 2

    # Error messages
    path_error_mes = "Data with name {%s} is not founded"
    country_error_mes = "Country with code {%s} is not founded"


    def __init__(self, subcode: int=0, message: str="Unknown build.sh error"):
        self.code = subcode
        self.message = message
