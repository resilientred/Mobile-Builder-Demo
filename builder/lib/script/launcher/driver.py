import logging
import os

from backend.model.helper.app_helper import parse_sku
from builder.lib.model.entity.driver_app import DriverApplication
from builder.lib.script.configurator.driver_configurator import AndroidDriverConfigurator
from std.mail.mail import Mail
from std.mail.mail_factory import MailFactory
from builder.lib.model.entity.letter import Letter
from builder.lib.model.helper.letter_builder import LetterBuilder
from builder.lib.script.builder import android_builder
from builder.lib.script.directory.directory_helper import DirectoryHelper
from builder.lib.script.launcher.launcher import Launcher
from builder.lib.script.resource.android_resource import AndroidResourceHelper

from std import config
from std.error import build_error
from std.error.build_error import BuildError
from std.mail.mail_info import MAIL_BUILD_SUCCESS
from std.std import validate_field, merge
from std.network import build_params_scheme


class AndroidDriverLauncher(Launcher):

    def __init__(self, application, params):
        # Entity
        self.application: DriverApplication = application

        # Build params
        self.need_build = validate_field(params[build_params_scheme.id_need_build])
        self.need_clear = validate_field(params[build_params_scheme.id_need_clear])
        self.create_app = validate_field(params[build_params_scheme.id_create_app])
        self.version_name = validate_field(params[build_params_scheme.id_version_name])
        self.version_code = validate_field(params[build_params_scheme.id_version_code])
        self.bundle = validate_field(params[build_params_scheme.id_def_bundle])
        self.email = validate_field(params[build_params_scheme.id_email])

        # Build paths
        self.finish_path = self.get_final_path(application.bundle)
        self.params_path = self.get_android_params_path(self.finish_path, application.bundle)
        self.res_path = merge(config.RES_PATH, application.bundle)

        self.new_bundle = application.bundle


    def generate(self):
        if self.create_app:
            dir_helper = DirectoryHelper(final_path=self.finish_path, root_path=self.get_root_path())
            self._prepare_dirs(dir_helper)

            res_helper = AndroidResourceHelper(path_to_res=self.res_path, final_path=self.finish_path)
            self._prepare_res(res_helper)

            config_helper = AndroidDriverConfigurator(file_path=self.params_path)
            self._prepare_config(config_helper)

        if self.need_build:
            self._build_app()
            self.send_apk(self.email, self.get_apk_path(self.application.bundle), "Driver", self.version_name)

        if self.need_clear:
            pass
            # self.clean_app(dir_helper)


    def _prepare_dirs(self, dir_helper):
        try:
            dir_helper.copy_sample_project()
        except FileExistsError:
            dir_helper.remove_final_project()
            dir_helper.copy_sample_project()
        dir_helper.replace_android_driver_bundle(self.new_bundle)
        dir_helper.replace_strings(bundle=self.bundle, new_bundle=self.new_bundle)
        dir_helper.replace_app_driver_dirs(app_name_id=parse_sku(self.new_bundle), bundle=self.new_bundle)  # TODO get app_sku from bundle


    def _prepare_res(self, res_helper):
        res_helper.replace_mipmap("ic_launcher")
        res_helper.replace_drawable("splash")
        res_helper.replace_drawable("gootax")
        res_helper.replace_drawable("push")

        res_helper.replace_google_driver_service()
        res_helper.replace_google_key_driver(self.application.google_map_key)
        res_helper.replace_app_name(self.application.app_name, type="driver")


    def _prepare_config(self, config_helper):
        config_helper.configure_by_app(self.application)


    def _build_app(self):
        android_builder.change_app_version(self.finish_path, self.version_name, self.version_code)
        android_builder.build_android_project(self.finish_path, assets_path=config.ASSETS_ANDROID_PATH,
                                              release_params=config.RELEASE)


    def send_apk(self, addressee, apk, type, version):
        letter: Letter = LetterBuilder.create_android_letter(type=type,
                                                             version=version,
                                                             sender=config.MAIL_LOGIN,
                                                             addressee=addressee,
                                                             message=MAIL_BUILD_SUCCESS,
                                                             app_name=self.application.app_name,
                                                             apk_path=apk)

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
            if 'app_android_driver' in path:  # TODO
                path = merge(config.ROOT_PATH, path)
                if not os.path.exists(path):
                    raise BuildError(build_error.path_error, build_error.path_error_mes % path)
                logging.info("Root " + path)
                return path


    @staticmethod
    def get_apk_path(bundle):
        path = merge(AndroidDriverLauncher.get_final_path(bundle), "app/build/outputs/apk/app-release.apk")
        logging.info("APK path " + path)
        return path


    # GET PATH TO FINAL PROJECT
    @staticmethod
    def get_final_path(bundle):
        path = merge(config.FINISH_PATH, "app_android_driver_" + bundle.replace(".", "_"))
        logging.info("Final " + path)
        return path


    # GET PATH TO AppParams.java
    @staticmethod
    def get_android_params_path(finish_path, bundle):
        app_params = "AppParams.java"
        path = str(bundle).replace(".", "/")
        path = merge(finish_path, "/app/src/main/java", path, "helper", app_params)
        logging.info("Params " + path)
        return path
