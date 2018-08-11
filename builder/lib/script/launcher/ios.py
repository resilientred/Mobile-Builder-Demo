import json
import logging
import os

from builder.lib.script.builder.ios_builder import IosBuilder
from builder.lib.script.configurator.ios_configurator import IosConfigurator
from builder.lib.script.directory.directory_helper import DirectoryHelper
from builder.lib.script.resource.ios_resource import IosResourceHelper

from std.mail.mail import Mail
from std.mail.mail_factory import MailFactory
from builder.lib.model.entity.letter import Letter
from builder.lib.model.helper.letter_builder import LetterBuilder
from std.mail.mail_info import MAIL_BUILD_SUCCESS

from backend.util.manager import asset_man as am
from builder.lib.model.entity.app import Application
from std import config
from std.error import build_error
from std.error.build_error import BuildError
from std.std import validate_field, merge
from std.network import build_params_scheme


class IosLauncher:
    def __init__(self, application, theme, params):
        self.application: Application = application
        self.theme = theme
        logging.debug(application)
        logging.debug(theme)

        # Build params
        self.need_build = validate_field(params[build_params_scheme.id_need_build])
        self.need_clear = validate_field(params[build_params_scheme.id_need_clear])
        self.create_app = validate_field(params[build_params_scheme.id_create_app])
        self.version_name = validate_field(params[build_params_scheme.id_version_name])
        self.version_code = validate_field(params[build_params_scheme.id_version_code])
        self.bundle = validate_field(params[build_params_scheme.id_def_bundle])
        self.email = validate_field(params[build_params_scheme.id_email])
        self.ios_company_name = validate_field(params[build_params_scheme.ios_company_name])
        self.id_build_email = validate_field(params[build_params_scheme.id_build_email])
        self.id_company_id = validate_field(params[build_params_scheme.id_company_id])

        # Build paths
        self.finish_path = self.get_final_path(application.bundle_ios)
        self.params_path = self.get_ios_params_path(self.finish_path)
        self.constants_path = self.get_ios_constant_path(self.finish_path)
        self.launch_screen_path = self.get_ios_launch_path(self.finish_path)
        self.res_path = merge(config.RES_PATH, application.bundle)

        self.country = am.get_country(application.country)
        self.new_bundle = application.bundle_ios


    def generate(self):
        res_helper = IosResourceHelper(assets_ios=config.ASSETS_IOS_PATH,
                                       path_to_res=self.res_path,
                                       finish_path=self.finish_path)
        if self.create_app:
            # Prepare Directory
            dir_helper = DirectoryHelper(final_path=self.finish_path, root_path=self.get_root_path())
            self._prepare_dirs(dir_helper)
            logging.debug("Prepare dirs")

            # Prepare Resources
            self._prepare_res(res_helper)
            logging.debug("Prepare res")

            # Prepare Config
            config_helper = IosConfigurator(file_path=self.params_path, constant_path=self.constants_path)
            self._prepare_config(config_helper)
            logging.debug("Prepare config")


        if self.need_build:
            res_helper.replace_short_version(self.version_code)
            res_helper.replace_version(self.version_name)

            ios_builder = IosBuilder(application=self.application,
                                     apple_id=self.id_build_email,
                                     assets_path=config.ASSETS_IOS_PATH,
                                     team_name=self.ios_company_name)
            self._build_app(ios_builder)


    def _build_app(self, ios_builder):
        ios_builder.create_ios_app()
        ios_builder.create_ios_dev(output_path=merge(self.res_path, "/cert"))
        ios_builder.create_ios_cert("3colors", self.res_path)
        ios_builder.create_ios_provision(output_path=merge(self.res_path, "/provision"))
        ios_builder.replace_ios_provision(file_path=merge(self.finish_path, '/Client.xcodeproj/project.pbxproj'))
        ios_builder.replace_distribution_cert(
            file_path=merge(self.finish_path, '/Client.xcodeproj/project.pbxproj'),
            company_id=self.id_company_id
        )

        ios_builder.build_ios_app(workspace_path=merge(self.finish_path, "/Client.xcworkspace"),
                                  output_path=config.TEMP_PATH,
                                  name=self.application.app_sku + ".ipa")

        ios_builder.upload_ios_app(ipa_path=merge(config.TEMP_PATH, self.application.app_sku + ".ipa"),
                                   app_version=self.version_code,
                                   build_number=self.version_name)

        logging.debug("Start sending certificate")
        path_to_cert = merge(self.res_path, self.application.bundle_ios + ".p12")
        if os.path.exists(path_to_cert):
            self.__send_push_cert(self.email, path_to_cert)
        logging.debug("End sending certificate")


    def _prepare_config(self, config_helper):
        config_helper.configure_by_app(self.application)


    def _prepare_res(self, res_helper):
        logo_splash = "logo_splash"
        menulogo = "menulogo"

        res_helper.replace_launch_image(logo_splash)
        res_helper.replace_image_set(menulogo)
        res_helper.replace_logo()
        del self.theme["id"]
        res_helper.put_color_scheme(merge(self.finish_path, "/Client/Helpers/Colors.swift"), json.dumps(self.theme))
        res_helper.replace_colors(screen_path=self.launch_screen_path,
                                  splash_color=self.theme["splash_bg"])
        res_helper.replace_project_name(self.application.app_name)


    def _prepare_dirs(self, dir_helper):
        if os.path.exists(self.finish_path):
            dir_helper.remove_final_project()
        dir_helper.copy_sample_project()
        dir_helper.replace_ios_bundle(self.bundle, self.new_bundle)


    def __send_push_cert(self, addressee, path_to_cert):
        letter: Letter = LetterBuilder.create_ios_cert_letter(sender=config.MAIL_LOGIN,
                                                              addressee=addressee,
                                                              message=MAIL_BUILD_SUCCESS,
                                                              app_name=self.application.app_name,
                                                              path_to_cert=path_to_cert)

        mail: Mail = MailFactory.getMail(config.MAIL_TYPE)
        mail.connect(config.MAIL_LOGIN, config.MAIL_PASSWORD)
        mail.send_letter(letter)
        mail.disconnect()


    @staticmethod
    def clean_app(dir_helper):
        dir_helper.remove_final_project()


    # GET PATH TO DEFAULT(MASTER) PROJECT
    @staticmethod
    def get_root_path():
        list_on_dir = os.listdir(config.ROOT_PATH)
        if len(list_on_dir) < 0:
            # EXCEPTION
            raise IndexError("get_sample_project_path, list_on_dir have size " + str(len(list_on_dir)))
        for path in list_on_dir:
            if 'ios_gootax_client' in path:
                path = merge(config.ROOT_PATH, path)
                if not os.path.exists(path):
                    raise BuildError(build_error.BuildError.path_error, build_error.BuildError.path_error_mes % path)
                logging.info("Root " + path)
                return path

    # GET PATH TO FINAL PROJECT
    @staticmethod
    def get_final_path(bundle: str):
        path = merge(config.FINISH_PATH, "gootax_app_ios_" + bundle.replace(".", "_"))
        logging.info("Final " + path)
        return path


    # GET PATH TO AppParams.java
    @staticmethod
    def get_ios_params_path(finish_path):
        app_params = "Config.swift"
        path = merge(finish_path, "/Client/Helpers/", app_params)
        logging.info("Params " + path)
        return path


    # GET PATH TO Constants.swift
    @staticmethod
    def get_ios_constant_path(finish_path):
        app_params = "Constants.swift"
        path = merge(finish_path, "/Client/Helpers/", app_params)
        logging.info("Params " + path)
        return path


    # GET PATH TO AppParams.java
    @staticmethod
    def get_ios_launch_path(finish_path):
        launch_screen = "LaunchScreen.storyboard"
        path = merge(finish_path, "/Client/Base.lproj/", launch_screen)
        logging.info("Launch screen path " + path)
        return path
