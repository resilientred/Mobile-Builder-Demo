from backend.model.entity.build import Build
from std.error.base_error import BaseError
from std.error.data_error import DataError
from std.std import validate_field, str_to_bool
from std.network import build_params_scheme


def generate_build_params(form: dict, root_bundle: str) -> dict:
    try:
        version_code = str(validate_version(form["version_code"])).strip()
        version_name = str(validate_version(form["version_name"])).strip()
        email = str(validate_email(form["email"])).strip()
        ios_company_name = str(validate_field(form["ios_company_name"])).strip()
        is_build = str_to_bool(validate_field(form["build_market"]))
        is_create_app = str_to_bool(form["create_app"])
        id_build_email = str(validate_email(form["build_email"])).strip()
        id_company_id = str(validate_field(form["company_id"])).strip()
        branch = str(validate_field(form["branch"])).strip()
    except BaseError as e:
        raise e

    build_params = {
        build_params_scheme.id_need_build: is_build,
        build_params_scheme.id_create_app: is_create_app,
        build_params_scheme.id_need_clear: True,
        build_params_scheme.id_def_bundle: root_bundle,
        build_params_scheme.id_version_code: version_code,
        build_params_scheme.id_version_name: version_name,
        build_params_scheme.id_email: email,
        build_params_scheme.ios_company_name: ios_company_name,
        build_params_scheme.id_build_email: id_build_email,
        build_params_scheme.branch: branch,
        build_params_scheme.id_company_id: id_company_id
    }

    return build_params


def generate_driver_build(form: dict, root_bundle: str) -> dict:
    try:
        version_code = str(validate_version(form["version_code"])).strip()
        version_name = str(validate_version(form["version_name"])).strip()
        email = str(validate_email(form["email"])).strip()
        is_build = str_to_bool(validate_field(form["build_market"]))
        branch = str(validate_field(form["branch"])).strip()
        is_create_app = str_to_bool(form["create_app"])
    except BaseError as e:
        raise e

    build_params = {
        build_params_scheme.id_need_build: is_build,
        build_params_scheme.id_create_app: is_create_app,
        build_params_scheme.id_need_clear: True,
        build_params_scheme.id_def_bundle: root_bundle,
        build_params_scheme.id_version_code: version_code,
        build_params_scheme.id_version_name: version_name,
        build_params_scheme.branch: branch,
        build_params_scheme.id_email: email,
    }

    return build_params


def generate_build(form: dict, app_id: int, theme_id: int, build_type: str, priority: int) -> Build:
    try:
        version_code = str(validate_version(form["version_code"]))
        version_name = str(validate_version(form["version_name"]))
        email = str(validate_email(form["email"]))
        is_build = str_to_bool(validate_field(form["build_market"]))
        is_create_app = str_to_bool(form["create_app"])

        build = Build(app_id=app_id, is_build=is_build, is_create=is_create_app, version_code=version_code,
                      version_name=version_name, is_clear=False, email=email, build_type=build_type, theme_id=theme_id,
                      status=Build.STATUS_WAITING, priority=priority, default_bundle='com.gootax.client')

        return build
    except BaseError as error:
        raise error


def validate_version(version: str) -> str:
    if version is None or len(version) > 20:
        raise DataError(DataError.not_found, DataError.version_invalid_mes % version)
    return version


def validate_email(email: str) -> str:
    if not email or "@" not in email or "." not in email:
        raise DataError(DataError.not_found, DataError.data_invalid_mes % email)
    return email

