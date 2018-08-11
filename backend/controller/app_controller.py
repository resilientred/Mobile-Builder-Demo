import json

import logging
import os
import traceback

from flask import Blueprint, render_template, redirect, request, make_response, Response, send_file

from backend.model.entity.app import Application
from backend.model.helper import app_helper
from backend.model.helper import theme_helper
from backend.model.helper.app_helper import validate_bundle
from backend.model.repository import theme_rep
from backend.model.repository.app_rep import ApplicationRepository

from backend.util.action.base_action import BaseAction
from backend.util.action.build_action import BuildAction
from backend.util.manager.res_man import ResourceManager
from builder.lib.script.launcher.android import AndroidLauncher
from builder.lib.script.launcher.ios import IosLauncher

from std import config
from std.error.base_error import BaseError
from std.error.db_error import DataBaseError
from std.network import api
from std.std import merge, sort_dict, validate_field


app_controller = Blueprint(
    name="app",
    import_name=__name__
)


# Get info about existing app config
@app_controller.route(api.get_app_info, methods=[api.get])
def get_app_info(app_id: int):
    # Init variables
    country_path = merge(config.ASSETS_PATH, 'phonecodes.json')
    try:
        # Variables for database
        app_db = ApplicationRepository(config.DATA_URL)
        theme_db = theme_rep.ThemeRepository(config.DATA_URL)

        # Get application from DB
        application = app_db.get_app_by_id(app_id)
        # Get theme from DB
        theme = theme_db.get_theme_by_hash(application.theme)
        theme_dict = sort_dict(theme.dict())  # Theme to dict

        # Remove in further
        del theme_dict['id']
        del theme_dict['hash']

        # Generate double quotes
        theme_dict = json.dumps(theme_dict)
        logging.info("Theme for " + application.app_name.upper() + " | " + theme_dict)

        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)
        res_saved = res_man.validate_resources(application.bundle, with_remote=False)  # TODO with remote True

        path = AndroidLauncher.get_final_path(application.bundle)  # TODO from this
        is_android_existing = os.path.exists(path)

        path = IosLauncher.get_final_path(application.bundle_ios)
        is_ios_existing = os.path.exists(path)

        # Read countries list
        with open(country_path) as data_file:
            countries = json.load(data_file)
    except Exception as e:
        traceback.print_exc()
        error_response = BaseError.generate_base_error(data=e.args)
        logging.error(error_response)

        # Render View
        return error_response

    response: Response = make_response(render_template("app-info.html",
                                                       app=application,
                                                       colors=theme_dict,
                                                       countries=countries,
                                                       android_res=res_saved["android"] or False,
                                                       ios_res=res_saved["ios"] or False,
                                                       google_res=res_saved["google"] or False))

    response.set_cookie("is_android_existing", str(is_android_existing or False))
    response.set_cookie("is_ios_existing", str(is_ios_existing or False))

    # Render View
    return response


# Get all existing applications and return for display
@app_controller.route(api.get_app_list, methods=[api.get])
def get_app_list():
    # Variables for database
    app_db = ApplicationRepository(config.DATA_URL)

    # Application
    apps = app_db.get_all_apps()

    # Render View
    return render_template("app-list.html",
                           apps=apps)


# Get all existing applications and return for display
@app_controller.route(api.app_list, methods=[api.get])
def app_list():
    # Variables for database
    app_db = ApplicationRepository(config.DATA_URL)

    # Application
    apps = app_db.get_all_apps()

    apps_json = []
    for appl in apps:
        apps_json.append(appl.get_simple_dist())
    # Render View
    return json.dumps(apps_json)


# Return form for creating new config
@app_controller.route(api.get_app_create, methods=[api.get])
def get_app_create():
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
    return render_template("app-create.html", countries=countries)


# Create new application
@app_controller.route(api.post_app_save, methods=[api.post])
def app_save():
    if request.method == api.post:
        try:
            # Variables for database
            app_db = ApplicationRepository(config.DATA_URL)
            theme_db = theme_rep.ThemeRepository(config.DATA_URL)

            # Init Resource Manager
            res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)

            try:
                app_helper.validate_app_fields(request.form)
                parsed_theme = theme_helper.get_theme_from_data(request.form)
                theme_helper.validate_theme_fields(parsed_theme)
            except BaseError as e:
                error_response = e.generate_error()
                logging.error(error_response)
                return error_response

            # Theme
            theme = theme_helper.parse_theme(sort_dict(parsed_theme))  # Sort dict

            # Application
            result = app_helper.generate_app_json(request.form, theme.hash)  # Form -> JSON
            print(result)
            new_app = app_helper.parse_app_by_json(result)  # JSON -> App
            old_app = app_db.get_app_by_bundle(new_app.bundle)  # Get Old App

            # Redirect if exist
            if old_app:
                return BaseError.generate_base_error(f"Application with Bundle - {new_app.bundle} already exist")

            try:
                app_db.create_app(new_app)  # Create app in DB
                theme_db.update_theme(theme)  # Create theme in DB
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
                                           data=BuildAction.data_created_build(api.get_app_list))


@app_controller.route("/test_image/<bundle>")
def test_image(bundle):
    path_bundle = str(bundle).replace(".", "_")
    path_to_image = merge(config.STATIC_PATH, "/apps", path_bundle + ".png")
    is_bundle_valid = validate_bundle(bundle)
    if is_bundle_valid and os.path.exists(path_to_image):
        return send_file(path_to_image, mimetype='image/png')
    else:
        return send_file(merge(config.STATIC_PATH, "/icon/default.png"), mimetype='image/png')


# Update existing application
@app_controller.route(api.post_app_update, methods=[api.post])
def app_update():
    if request.method == api.post:
        # Init Resource Manager
        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)

        try:
            app_helper.validate_app_fields(request.form, check_id=True)
            parsed_theme = theme_helper.get_theme_from_data(request.form)
            theme_helper.validate_theme_fields(parsed_theme)
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
            app_db = ApplicationRepository(config.DATA_URL)
            theme_db = theme_rep.ThemeRepository(config.DATA_URL)

            # Theme
            theme = theme_helper.parse_theme(sort_dict(parsed_theme))  # Dict -> Sort dict -> Theme

            # Application
            old_app = app_db.get_app_by_id(index)  # App from index
            old_bundle = old_app.bundle  # old sku

            result = app_helper.generate_app_json(request.form, theme.hash)  # Form -> JSON
            application = app_helper.parse_app_by_json(result)  # JSON -> App
            application.id = index

            # Commit DB
            app_db.update_app(application)  # Update app in DB
            theme_db.update_theme(theme)  # Update theme in DB
        except Exception as e:
            return DataBaseError(subcode=DataBaseError.duplicate_code, data=e.args).generate_error()

        try:
            res_man.update_app_res(request.files, old_bundle, application.bundle)  # Update Res
            ResourceManager.create_app_icon(request.files, config.STATIC_PATH, application.bundle)
            return redirect(merge(api.get_app_info_num, index))
        except BaseError as e:
            traceback.print_exc()
            error_response = e.generate_error()
            logging.error(error_response)
            return error_response

    return redirect(api.get_app_list)


@app_controller.route(api.app_delete, methods=[api.post])
def app_delete():
    if request.method == api.post:
        form = request.form
        index = validate_field(form["id"])

        app_db = ApplicationRepository(config.DATA_URL)
        res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)
        application = app_db.get_app_by_id(index)  # App DICT from DB

        app_db.delete_app(application)
        res_man.delete_res(application.bundle)  # Delete app res

    return redirect(api.get_app_list)
