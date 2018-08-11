"""

THIS FILE MAYBE USING ONLY INSIDE main.py AND route.py AND queue.py

"""
import os

from std.mail.mail import GOOGLE_MAIL
from std.std import merge


# ---------- COMMON SETTINGS
# Debug mode application

IS_DEBUG: bool = True

# Root project path - MASK: XXX/python-build.sh-project
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Need generate new bundle
ROOT_BUNDLE: str = 'com.gootax.client'
ROOT_BUNDLE_DRIVER: str = 'com.gootax.driver'
RESOURCE_PATH: str = "/Users/andrew/PycharmProjects/python-build-script-res/resource"  # TODO CHANGE RES PATH3
RES_PATH: str = merge(RESOURCE_PATH, "res")  # Path to resources for build.sh projects
COMMON_ASSETS_PATH: str = merge(BASE_DIR, "std/assets")

ROOT_PATH: str = merge(RESOURCE_PATH, "master")  # Path to root Android and iOS client project
FINISH_PATH: str = "/Volumes/Macintosh/builder/result"  # Path to final Android and iOS client project

QUEUE_NAME: str = "test1"

MAIL_TYPE: str = GOOGLE_MAIL
MAIL_LOGIN: str = "gootax.mobile@gmail.com"
MAIL_PASSWORD: str = "asdzxccxzdsa"

DRIVE_SECRET_PATH: str = merge(BASE_DIR, "std/assets/client_secrets.json")
DRIVE_CREDENTIALS_PATH: str = merge(BASE_DIR, "std/assets/credentials.json")
DRIVE_SETTINGS_PATH: str = merge(BASE_DIR, "std/assets/settings.yaml")

TELEGRAM_SECRET: str = '324952871:AAEI94LF9VitVYdKARABxknQSJKy4vHUymA'

# ---------- SERVER SETTINGS
LOGGING_MASK: str = u'[%(asctime)s] %(filename)s[LINE:%(lineno)d] #%(levelname)-4s %(message)s'
LOGGING_FILE: str = merge(RESOURCE_PATH, "log/logging.log")

TEMP_PATH: str = merge(RESOURCE_PATH, "tmp")  # For temp save files

TEMPLATE_PATH: str = merge(BASE_DIR, "/frontend/templates")  # For HTML
STATIC_PATH: str = merge(BASE_DIR, "/frontend/static")  # For CSS and Fonts
ASSETS_PATH: str = merge(BASE_DIR, "/frontend/assets")

MAX_SIZE_FILE: int = 16 * 1024 * 1024  # 16 MB
KEEP_FINAL_TIME: int = 60 * 60 * 24  # 1 Day

HOST: str = "192.168.1.55"  # TODO CHANGE HOST
BASE_URL: str = "http://" + HOST + ":5000"

DATA_URL: str = 'mysql://mobilebuilder:JneijSj39ZmnqkwSDew@db2.taxi.lcl/mobilebuilder?charset=utf8'
# DATA_URL: str = 'mysql://root@127.0.0.1/mobilebuilder?charset=utf8'
# DATA_URL: str = 'mysql://root:123123@localhost/build_script?charset=utf8'


# ---------- BUILDER SETTINGS

HOST_BUILDER: str = HOST  # TODO CHANGE HOST
BASE_BUILDER_URL: str = "http://" + HOST + ":5001"

# ---------- IOS SETTINGS
# Path to ios assets
ASSETS_IOS_PATH: str = merge(BASE_DIR, "builder/lib/assets/ios")  # Path to Android assets

IOS_REP: str = "https://mgootax_redmine@bitbucket.org/3colors/gootax_app_ios_client_swift3.git"
IOS_FOLDER_NAME: str = "ios_gootax_client"
IOS_MASTER_PATH: str = merge(ROOT_PATH, IOS_FOLDER_NAME)

TEAM_NAME: str = "Gootax OOO"

ANDROID_DRIVER_REP: str = "https://mgootax_redmine@bitbucket.org/gootaxapp/app_android_driver.git"
ANDROID_DRIVER_FOLDER_NAME: str = "app_android_driver"
ANDROID_DRIVER_MASTER_PATH: str = merge(ROOT_PATH, ANDROID_DRIVER_FOLDER_NAME)

# ---------- ANDROID SETTINGS
# Path to android assets
ASSETS_ANDROID_PATH: str = merge(BASE_DIR, "builder/lib/assets/android")  # Path to Android assets

ANDROID_REP: str = "https://mgootax_redmine@bitbucket.org/3colors/gootax_app_android_client_v3.git"
ANDROID_FOLDER_NAME: str = "android_gootax_client"
ANDROID_MASTER_PATH: str = merge(ROOT_PATH, ANDROID_FOLDER_NAME)

COUNTRY_LIST = ["", "-ru", "-fa", "-az", "-tk", "-uz", "-ka", "-sr", "-me", "-it", "-de", "-tg", "-ar", "-ky"]
COUNTRY_DRIVER_LIST = ["", "-uz", "-tk", "-sr", "-sr-rME", "-ru", "-ro", "-ka", "-ga", "-fi", "-fa", "-de", "-cs", "-az", "-ar"]


# Info for release data build.sh
RELEASE: dict = {
    "KEY_FILE": merge(BASE_DIR, "builder/lib/assets/android/myandroid.keystore"),
    "FILE_PASS": "asdzxc",
    "KEY_ALIAS": "myandroid",
    "ALIAS_PASS": "asdzxc",
}

# Need for generate local.properties
SDK_PATH: str = "/Users/andrew/Library/Android/sdk"  # TODO CHANGE SDK PATH
NDK_PATH: str = "/Users/andrew/Library/Android/sdk/ndk-bundle"  # TODO CHANGE NDK (NOT USING)

# SDK_PATH = "/Users/santa/Library/Android/sdk"
# NDK_PATH = "/Users/santa/Library/Android/sdk/ndk-bundle"

# ----------- MOBILE SETTINGS

REPOSITORIES: dict = {
    "ios": IOS_REP,
    "android": ANDROID_REP,
    "android_driver": ANDROID_DRIVER_REP
}

MASTER_PATH: dict = {
    "ios": IOS_MASTER_PATH,
    "android": ANDROID_MASTER_PATH,
    "android_driver": ANDROID_DRIVER_MASTER_PATH
}

