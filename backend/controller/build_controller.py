import json

import logging
import traceback

from flask import Blueprint, request, render_template

from backend.model.entity.app import Application
from backend.model.helper import build_helper
from backend.model.repository.app_rep import ApplicationRepository
from backend.model.repository.build_rep import BuildRepository
from backend.model.repository.driver_app_repository import DriverApplicationRepository

from backend.network.queue.producer.build import BuildProducer

from backend.util.action.base_action import BaseAction
from backend.util.action.build_action import BuildAction
from backend.util.manager.res_man import ResourceManager

from backend.model.repository import theme_rep

from std.error.base_error import BaseError
from std.network import api

from std import config
from std.std import validate_field


build_controller = Blueprint(
    name="build",
    import_name=__name__
)


# Get all existing applications and return for display
@build_controller.route(api.build_list, methods=[api.get])
def build_list():
    build_rep = BuildRepository(config.DATA_URL)
    builds = build_rep.get_active_asc_priority()
    return render_template("build-list.html", builds=builds)


# Get all existing applications and return for display
@build_controller.route(api.build_info, methods=[api.get])
def build_info(build_id):
    build_rep = BuildRepository(config.DATA_URL)
    build = build_rep.get_build_by_id(build_id)
    return render_template("build-info.html", build=build)


# Get all existing applications and return for display
@build_controller.route(api.build_history, methods=[api.get])
def build_history():
    build_rep = BuildRepository(config.DATA_URL)
    builds = build_rep.get_complete_builds()
    return render_template("build-list.html", builds=builds)


# Method for build.sh application
@build_controller.route(api.post_app_build, methods=[api.post])
def app_build():
    if request.method == api.post:
        logging.info(request.form)

        try:
            form = request.form
            build_type = validate_field(form["build_type"])
            index = validate_field(form["id"])

            is_ios: bool = False
            is_android: bool = False

            if build_type == "ios":
                is_ios = True
            elif build_type == "android":
                is_android = True
            # create_app: bool = str_to_bool(validate_field(form["create_app"]))

            build_params = build_helper.generate_build_params(form, config.ROOT_BUNDLE)
        except BaseError as e:

            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

        # Variables for database
        app_db = ApplicationRepository(config.DATA_URL)
        theme_db = theme_rep.ThemeRepository(config.DATA_URL)

        application = app_db.get_app_by_id(index)  # App DICT from DB
        theme = theme_db.get_theme_by_hash(application.theme)  # Theme from DB

        res_man = ResourceManager(config.RESOURCE_PATH, config.TEMP_PATH)
        res_saved = res_man.validate_resources(application.bundle)
        print(res_saved)

        producer = BuildProducer(config.QUEUE_NAME)
        producer.connect()
        if is_ios:
            message = BuildProducer.generate_message(application, theme, build_params, build_type="ios")
            logging.info("For rabbit producer generated Message {%s}" % message)
            producer.send(message=message)
        elif is_android:
            message = BuildProducer.generate_message(application, theme, build_params, build_type="android")
            logging.info("For rabbit producer generated Message {%s}" % message)
            producer.send(message=message)
            producer.disconnect()

        # application.status = Application.STATUS_WAITING
        app_db.update_app(application)

    return BuildAction.create_action_build(action=BaseAction.REDIRECT_ACTION,
                                           subcode=BuildAction.BUILD_CREATED,
                                           data=BuildAction.data_created_build(api.get_build_info))


@build_controller.route(api.post_update_build_status, methods=[api.post])
def build_update():
    # Variables for database
    app_db = ApplicationRepository(config.DATA_URL)
    logging.info("Build updating " + str(request.form))
    data = request.form
    app_index = validate_field(data["app_index"])
    status = validate_field(data["status"])
    # TODO REWORK THIS! It is not best practices
    application = app_db.get_app_by_id(app_index)
    application.status = status
    app_db.update_app(application)
    return ""


@build_controller.route(api.post_driver_update_build_status, methods=[api.post])
def build_update_driver():
    # Variables for database
    app_db = DriverApplicationRepository(config.DATA_URL)
    logging.info("Build updating " + str(request.form))
    data = request.form
    app_index = validate_field(data["app_index"])
    status = validate_field(data["status"])
    # TODO REWORK THIS! It is not best practices
    application = app_db.get_app_by_id(app_index)
    application.status = status
    app_db.update_app(application)
    return ""


def app_build_test():
    if request.method == api.post:
        logging.info(request.form)

        try:
            form = request.form
            build_type = validate_field(form["build_type"])
            index = validate_field(form["id"])
        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

        # Variables for database
        app_db = ApplicationRepository(config.DATA_URL)
        theme_db = theme_rep.ThemeRepository(config.DATA_URL)

        application = app_db.get_app_by_id(index)  # App DICT from DB
        theme = theme_db.get_theme_by_hash(application.theme)  # Theme from DB

        res_man = ResourceManager(config.RESOURCE_PATH, config.TEMP_PATH)
        try:
            res_valid = res_man.validate_resources(application.bundle)
        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

        if res_valid:
            build_rep = BuildRepository(config.DATA_URL)
            active_builds_count = build_rep.get_active_builds_count() + 1
            build = build_helper.generate_build(form=form,
                                                app_id=application.app_id,
                                                build_type=build_type,
                                                theme_id=theme.id,
                                                priority=active_builds_count)
            build_rep.create_build(build)

        application.status = Application.STATUS_WAITING
        app_db.update_app(application)

    return BuildAction.create_action_build(action=BaseAction.REDIRECT_ACTION,
                                           subcode=BuildAction.BUILD_CREATED,
                                           data=BuildAction.data_created_build(api.get_build_info))


def app_build_test():
    if request.method == api.post:
        logging.info(request.form)

        try:
            form = request.form
            build_id = validate_field(form["build_id"])
            from_priority = validate_field(form["from_priority"])
            to_priority = validate_field(form["to_priority"])

            build_rep = BuildRepository(config.DATA_URL)
            builds = build_rep.get_active_desc_priority()

        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

    return ""
