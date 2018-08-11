import fileinput
import os
import re
import subprocess

from builder.lib.model.entity.app import Application
from std.std import merge


class IosBuildEnv:
    # Create
    APPLE_ID = "APPLE_ID"
    BUNDLE = "BUNDLE"
    APP_NAME = "APP_NAME"
    INIT_VERSION = "INIT_VERSION"
    SKU = "SKU"
    PLATFORM = "PLATFORM"
    LANGUAGE = "LANGUAGE"
    APPLE_TEAM_NAME = "APPLE_TEAM_NAME"
    ITUNES_TEAM_NAME = "ITUNES_TEAM_NAME"

    # Cert
    CERT_PASS = "CERT_PASS"
    CERT_FILE_NAME = "CERT_FILE_NAME"
    TEAM_NAME = "TEAM_NAME"
    OUTPUT_PATH = "OUTPUT_PATH"

    # Provision
    PROVISION_NAME_PROD = "PROVISION_NAME_PROD"
    OUTPUT_NAME_PROD = "OUTPUT_NAME_PROD"
    PROVISION_NAME_DEV = "PROVISION_NAME_DEV"
    OUTPUT_NAME_DEV = "OUTPUT_NAME_DEV"
    PROVISION_NAME_APPSTORE = "PROVISION_NAME_APPSTORE"
    OUTPUT_NAME_APPSTORE = "OUTPUT_NAME_APPSTORE"

    # Build
    OUTPUT_NAME = "OUTPUT_NAME"
    WORKSPACE_PATH = "WORKSPACE_PATH"
    BUILD_SCHEME = "BUILD_SCHEME"

    # Upload
    IPA_PATH = "IPA_PATH"
    APP_VERSION = "APP_VERSION"
    BUILD_NUMBER = "BUILD_NUMBER"


class IosBuilder:
    def __init__(self, application: Application, team_name, apple_id, assets_path):
        self.application = application
        self.apple_id = apple_id
        self.assets_path = assets_path
        self.team_name = team_name


    # Build final android project (Generate Release APK file)
    def create_ios_app(self):
        script_path = merge(self.assets_path, '/create_app.sh')

        params = os.environ

        params[IosBuildEnv.APPLE_ID] = self.apple_id  # Put path to final project in variables environment
        params[IosBuildEnv.BUNDLE] = self.application.bundle_ios
        params[IosBuildEnv.APP_NAME] = "Gootax" + self.application.app_sku
        params[IosBuildEnv.INIT_VERSION] = "1.0"
        params[IosBuildEnv.SKU] = self.application.app_sku
        params[IosBuildEnv.PLATFORM] = "ios"
        params[IosBuildEnv.LANGUAGE] = "Russian"
        params[IosBuildEnv.APPLE_TEAM_NAME] = self.team_name
        params[IosBuildEnv.ITUNES_TEAM_NAME] = self.team_name

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script


    # Build final android project (Generate Release APK file)
    def create_ios_cert(self, password, output_path):
        script_path = merge(self.assets_path, '/create_cert.sh')
        params = os.environ

        params[IosBuildEnv.BUNDLE] = self.application.bundle_ios
        params[IosBuildEnv.CERT_PASS] = password
        params[IosBuildEnv.CERT_FILE_NAME] = self.application.bundle_ios + ".pem"
        params[IosBuildEnv.TEAM_NAME] = self.team_name
        params[IosBuildEnv.OUTPUT_PATH] = output_path

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script


    # Generate ios dev and distribution certificates
    def create_ios_dev(self, output_path):
        script_path = merge(self.assets_path, '/create_dev.sh')
        params = os.environ

        params[IosBuildEnv.APPLE_ID] = self.apple_id
        params[IosBuildEnv.TEAM_NAME] = self.team_name
        params[IosBuildEnv.PLATFORM] = "ios"
        params[IosBuildEnv.OUTPUT_PATH] = output_path

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script


    # Build final android project (Generate Release APK file)
    def create_ios_provision(self, output_path):
        prod = "Prod"
        dev = "Dev"
        app_store = "AppStore"

        provision = ".mobileprovision"

        script_path = merge(self.assets_path, '/create_provisions.sh')
        params = os.environ

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        params[IosBuildEnv.BUNDLE] = self.application.bundle_ios
        params[IosBuildEnv.APPLE_ID] = self.apple_id
        params[IosBuildEnv.TEAM_NAME] = self.team_name
        params[IosBuildEnv.PLATFORM] = "ios"
        params[IosBuildEnv.OUTPUT_PATH] = output_path

        params[IosBuildEnv.PROVISION_NAME_PROD] = self.application.bundle_ios + prod
        params[IosBuildEnv.OUTPUT_NAME_PROD] = self.application.bundle_ios + prod + provision

        params[IosBuildEnv.PROVISION_NAME_DEV] = self.application.bundle_ios + dev
        params[IosBuildEnv.OUTPUT_NAME_DEV] = self.application.bundle_ios + dev + provision

        params[IosBuildEnv.PROVISION_NAME_APPSTORE] = self.application.bundle_ios + app_store
        params[IosBuildEnv.OUTPUT_NAME_APPSTORE] = self.application.bundle_ios + app_store + provision

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script


    def replace_ios_provision(self, file_path):
        appStore = "AppStore"
        SPECIFIER = "PROVISIONING_PROFILE_SPECIFIER"

        with fileinput.FileInput(file_path, inplace=True) as file:
            for line in file:
                if SPECIFIER in line:
                    print(str(SPECIFIER + " = " + self.application.bundle_ios + appStore + ";"), end='\n')
                else:
                    print(line, end='\n')


    # FIND REGEX
    @staticmethod
    def regex_psfs(key):
        return '^.*\s' + key + '\s=\s\"([^\"]+)\".*$'

    @staticmethod
    def regex_obj(key):
        return '^.*\s' + key + '\s*=\s*([^;]+).*$'


    def find_obj(self, text, key):
        return re.findall(self.regex_obj(key), text, flags=re.MULTILINE)

    # FIND FUNCTIONS
    def find_psfs(self, text, key):
        return re.findall(self.regex_psfs(key), text, flags=re.MULTILINE)


    def replace_distribution_cert(self, file_path, company_id):
        CODE_SIGN_IDENTITY = "CODE_SIGN_IDENTITY"
        DEVELOPMENT_TEAM = "DEVELOPMENT_TEAM"
        team = self.team_name
        distribution_name = f"iPhone Distribution: {team} ({company_id})"

        with fileinput.FileInput(file_path, inplace=True) as file:
            for line in file:
                group = self.find_psfs(line, CODE_SIGN_IDENTITY)
                group_corp = self.find_obj(line, DEVELOPMENT_TEAM)
                if len(group) > 0:
                    print(line.replace(group[0], str(distribution_name)), end='')
                elif len(group_corp) > 0:
                    print(line.replace(group_corp[0], str(company_id)), end='')
                else:
                    print(line, end='')
                    continue


    # Build final android project (Generate Release APK file)
    def build_ios_app(self, workspace_path, output_path, name):
        script_path = merge(self.assets_path, '/build.sh')
        params = os.environ

        params[IosBuildEnv.WORKSPACE_PATH] = workspace_path
        print(params[IosBuildEnv.WORKSPACE_PATH])
        params[IosBuildEnv.BUILD_SCHEME] = "Client"
        params[IosBuildEnv.OUTPUT_PATH] = output_path
        params[IosBuildEnv.OUTPUT_NAME] = name

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script


    # Build final android project (Generate Release APK file)
    def upload_ios_app(self, ipa_path, app_version, build_number):
        script_path = merge(self.assets_path, '/upload.sh')
        params = os.environ

        params[IosBuildEnv.APPLE_ID] = self.apple_id
        params[IosBuildEnv.BUNDLE] = self.application.bundle_ios
        params[IosBuildEnv.IPA_PATH] = ipa_path
        params[IosBuildEnv.TEAM_NAME] = self.team_name
        params[IosBuildEnv.APP_VERSION] = app_version
        params[IosBuildEnv.BUILD_NUMBER] = build_number

        print(params)

        subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
        subprocess.call([script_path], shell=True, env=params)  # Run script
