import json

from std.error.base_error import BaseError
from std.error.data_error import DataError
from std.std import validate_field

#PARAMS FOR BUILD
app_id = 'id'
is_ios = 'ios'
is_android = 'android'

is_create_app = 'create_app'

version_code = 'version_code'
version_name = 'version_name'
email = 'email'

build_android = 'build_android'
build_ios = 'build_ios'


def generate_build_params(params: dict) -> dict:
    try:
        app_id_valid = validate_field(params['i'])
        platform = validate_field(params['p'])
        version_code_valid = validate_version(validate_field(params['v']))
        version_number_valid = validate_version(validate_field(params['n']))
        email_valid = validate_email(parse_email(params.get('m')))
        is_create_app_valid = True

        if platform == 'android':
            is_build_android_valid = True
            is_android_valid = True
            is_build_ios_valid = False
            is_ios_valid = False
        elif platform == 'ios':
            is_build_android_valid = False
            is_android_valid = False
            is_build_ios_valid = True
            is_ios_valid = True
        else:
            raise AttributeError

        build_params = {
            app_id: app_id_valid,
            is_ios: is_ios_valid,
            is_android: is_android_valid,

            version_code: version_code_valid,
            version_name: version_number_valid,
            email: email_valid,

            build_android: is_build_android_valid,
            build_ios: is_build_ios_valid,
            is_create_app: is_create_app_valid,
        }

    except BaseError as e:
        raise e
    return json.dumps(build_params)


def validate_version(version: str) -> str:
    if version is None or len(version) > 11:
        raise DataError(DataError.not_found, DataError.data_invalid_mes % version)
    return version


def validate_email(email: str) -> str:
    if not email or "@" not in email or "." not in email:
        raise DataError(DataError.not_found, DataError.data_invalid_mes % email)
    return email


def parse_email(email, default='3colors@gmail.com'):
    print(email)
    if email is None or email == '':
        return default
    return email


def parse_application_status(status: int) -> str:
    if status == 1:
        return "Отправлено в очередь"
    elif status == 2:
        return "В очереди"
    elif status == 3:
        return "Выполняется"
    else:
        return "Неизвестно"


def parse_param_required(string, params):
    for param in params:
        if param == string:
            return params[string]
    raise AttributeError
