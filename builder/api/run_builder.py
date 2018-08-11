from flask import Flask
from flask import request
from std.std import validate_field
from std.error.base_error import BaseError
from builder.lib.script.launcher.android import AndroidLauncher
from builder.lib.script.launcher.ios import IosLauncher
from backend.util.action.base_action import BaseAction
import os
from std import config

builder = Flask(__name__)

# Request types
get = 'GET'
post = 'POST'

build_app = "/builder/build_app"
check_project_exist = "/builder/check_project_exist"


@builder.route(build_app, methods=[post])
def build_app():
    pass


@builder.route(check_project_exist, methods=[get])
def get_project_exist():
    try:
        bundle_ios = validate_field(request.args["bundle_ios"])
        bundle_android = validate_field(request.args["bundle_android"])

        path = AndroidLauncher.get_final_path(bundle_android)
        is_android_existing = os.path.exists(path)

        path = IosLauncher.get_final_path(bundle_ios)
        is_ios_existing = os.path.exists(path)

        return BaseAction.create_action(action=BaseAction.CHECK_ACTION,
                                        code=BaseAction.SUCCESS_CODE,
                                        subcode=BaseAction.CHECK_CREATED_SUBCODE,
                                        data={
                                            "is_android_existing": is_android_existing,
                                            "is_ios_existing": is_ios_existing
                                        })
    except BaseError as error:
        return error.generate_error()


if __name__ == "__main__":
    builder.run(host=config.HOST_BUILDER, port="5001")
