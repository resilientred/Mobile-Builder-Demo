# Author Andrew Chupin
# Coding in UTF-8
import traceback

import logging
from flask import Blueprint
from flask import Response
from flask import json
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request

from backend.model.entity.driver_app import DriverApplication
from backend.model.repository.driver_app_repository import DriverApplicationRepository
from backend.model.helper import driver_app_helper
from backend.network.queue.producer.build import BuildProducer
from backend.util.action.base_action import BaseAction
from backend.util.action.build_action import BuildAction
from backend.util.manager.res_man import ResourceManager
from std.error.base_error import BaseError
from std.error.db_error import DataBaseError
from std.network import api
from std import config
from std.std import merge, validate_field, str_to_bool


api_driver_app_list = "/driver_app_list"
api_driver_app_save = "/driver_app_save"
api_driver_app_info = "/driver_app_info/<app_id>"
api_driver_app_create = "/driver_app_create"
api_driver_app_update = "/driver_app_update"
api_driver_app_build = "/driver_app_build"
api_driver_app_delete = "/driver_app_delete"

driver_controller = Blueprint(
    name="driver",
    import_name=__name__
)


@driver_controller.route(api_driver_app_list, methods=[api.get])
def driver_app_list():
    # Variables for database
    app_db = DriverApplicationRepository(config.DATA_URL)

    # Application
    apps = app_db.get_all_apps()

    # Render View
    return render_template("driver-app-list.html",
                           apps=apps)


@driver_controller.route(api_driver_app_save, methods=[api.post])
def driver_app_save():
    if request.method == api.post:
        try:
            # Variables for database
            app_db = DriverApplicationRepository(config.DATA_URL)

            # Init Resource Manager
            res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)

            # Application
            result = driver_app_helper.generate_app_json(request.form)  # Form -> JSON
            print(result)
            new_app = driver_app_helper.parse_app_by_json(result)  # JSON -> App
            old_app = app_db.get_app_by_bundle(new_app.bundle)  # Get Old App

            # Redirect if exist
            if old_app:
                return BaseError.generate_base_error(f"Application with Bundle - {new_app.bundle} already exist")

            try:
                app_db.create_app(new_app)  # Create app in DB
            except Exception as e:
                return BaseError.generate_base_error(f"Error while saving application {e.args}")

            if request.files:
                try:
                    res_man.create_app_res(request.files, new_app.bundle)  # Create Resource # TODO BUNDLE
                except BaseError as e:
                    traceback.print_exc()
                    res_man.delete_res(new_app.bundle)  # Delete Resource if Error
                    error_response = e.generate_error()
                    logging.error(error_response)
                    return error_response
        except Exception as e:
            traceback.print_exc()
            error_response = BaseError.generate_base_error(data=e.args)
            logging.error(error_response)
            return error_response

    return BuildAction.create_action_build(action=BaseAction.REDIRECT_ACTION,
                                           subcode=BuildAction.BUILD_CREATED,
                                           data=BuildAction.data_created_build(api_driver_app_list))


@driver_controller.route(api_driver_app_info, methods=[api.get])
def driver_app_info(app_id: int):
    # Init variables
    country_path = merge(config.ASSETS_PATH, 'phonecodes.json')
    try:
        # Variables for database
        app_db = DriverApplicationRepository(config.DATA_URL)

        # Get application from DB
        application = app_db.get_app_by_id(app_id)
        print(application.app_name)
        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)
        res_saved = res_man.validate_resources(application.bundle, with_remote=False)  # TODO with remote True)
        print(res_saved)
        # Read countries list
        with open(country_path) as data_file:
            countries = json.load(data_file)
    except Exception as e:
        traceback.print_exc()
        error_response = BaseError.generate_base_error(data=e.args)
        logging.error(error_response)

        # Render View
        return error_response

    response: Response = make_response(render_template("driver-app-info.html",
                                                       app=application,
                                                       countries=countries,
                                                       android_driver=res_saved["android_driver"] or False,
                                                       google_driver=res_saved["google_driver"] or False
                                                       ))

    # Render View
    return response


@driver_controller.route(api_driver_app_create, methods=[api.get])
def driver_app_create():
    try:
        # Init variables
        country_assets = merge(config.ASSETS_PATH, 'phonecodes.json')

        # Read countries list
        with open(country_assets) as data_file:
            countries = json.load(data_file)
    except Exception as e:
        traceback.print_exc()
        error_response = BaseError.generate_base_error(data=e.args)
        logging.error(error_response)
        return error_response

    # Render View
    return render_template("driver-app-create.html", countries=countries)


@driver_controller.route(api_driver_app_build, methods=[api.post])
def driver_app_build():
    if request.method == api.post:
        logging.info(request.form)

        try:
            form = request.form
            build_type = validate_field(form["build_type"])
            index = validate_field(form["id"])

            from backend.model.helper import build_helper
            build_params = build_helper.generate_driver_build(form, config.ROOT_BUNDLE_DRIVER)
            logging.info(build_params)
        except BaseError as e:

            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

        # Variables for database
        app_db = DriverApplicationRepository(config.DATA_URL)

        application = app_db.get_app_by_id(index)  # App DICT from DB

        res_man = ResourceManager(config.RESOURCE_PATH, config.TEMP_PATH)
        res_saved = res_man.validate_resources(application.bundle)
        print(res_saved)

        producer = BuildProducer(config.QUEUE_NAME)
        producer.connect()
        message = BuildProducer.generate_driver_message(application, build_params, build_type=build_type)
        logging.info("For rabbit producer generated Message {%s}" % message)
        producer.send(message=message)
        producer.disconnect()

        app_db.update_app(application)

    return BuildAction.create_action_build(action=BaseAction.REDIRECT_ACTION,
                                           subcode=BuildAction.BUILD_CREATED,
                                           data=BuildAction.data_created_build(api_driver_app_list))


@driver_controller.route(api_driver_app_update, methods=[api.post])
def driver_app_update():
    if request.method == api.post:
        # Init Resource Manager
        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)

        try:
            from backend.model.helper import app_helper
            index = request.form[app_helper.FIELD_ID]
        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response
        except Exception as e:
            traceback.print_exc()
            error_response = BaseError.generate_base_error(data=e.args)
            logging.error(msg=error_response)
            return error_response

        try:
            # Variables for database
            app_db = DriverApplicationRepository(config.DATA_URL)


            # Application
            old_app = app_db.get_app_by_id(index)  # App from index
            old_bundle = old_app.bundle  # old sku

            print(f"form {request.form}")
            result = driver_app_helper.generate_app_json(request.form)  # Form -> JSON
            print(f"result {result}")
            application = driver_app_helper.parse_app_by_json(result)  # JSON -> App
            application.id = index

            # Commit DB
            app_db.update_app(application)  # Update app in DB
        except Exception as e:
            return DataBaseError(subcode=DataBaseError.duplicate_code, data=e.args).generate_error()

        try:
            res_man.update_app_res(request.files, old_bundle, application.bundle)  # Update Res
            ResourceManager.create_app_icon(request.files, config.STATIC_PATH, application.bundle)
            return redirect(f"/driver_app_info/{index}")
        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

    return redirect(api.get_app_list)


@driver_controller.route(api_driver_app_delete, methods=[api.post])
def app_delete():
    if request.method == api.post:
        form = request.form
        index = validate_field(form["id"])

        app_db = DriverApplicationRepository(config.DATA_URL)
        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)
        application = app_db.get_app_by_id(index)  # App DICT from DB

        app_db.delete_app(application)
        res_man.delete_res(application.bundle)  # Delete app res

    return redirect(api.get_app_list)