import fileinput
import re

from backend.model.entity import app

# This class parse and replace value in AppParams by key
TENANT_ID = "TENANT_ID"
API_KEY = "API_KEY"
APP_ID = "APP_ID"
PUSH_SENDER_ID = "PUSH_SENDER_ID"
METRICA_KEY = "METRICS_KEY"
URL = "URL"
GEO_URL = "GEO_URL"

IS_DEMO = "IS_DEMO"
FILL_SPLASH = "FILL_SPLASH"
USE_REFERRAL = "USE_REFERRAL"
USE_REVIEW_BLOCK = "USE_REVIEW_BLOCK"
WITH_COUNTRY = "WITH_COUNTRY"

USE_SEARCH = "USE_SEARCH"
ORDER_WITH_ONE_ADDRESS = "ORDER_WITH_ONE_ADDRESS"
WITH_MAX_ONE_ADDRESS = "WITH_MAX_ONE_ADDRESS"
AUTOCOMPLETE_RADIUS = "AUTOCOMPLETE_RADIUS"
REVERSE_RADIUS = "REVERSE_RADIUS"
WITH_EDIT_ORDER = "USE_EDIT_ORDER"
SHOWN_CLIENT_ID = "SHOWN_CLIENT_ID"
USE_REVIEW_DETAIL = "USE_REVIEW_DETAIL"
USE_REVIEW_FOR_REJECTED = "USE_REVIEW_FOR_REJECTED"

USE_PUBLIC_TRANSPORT = "USE_PUBLIC_TRANSPORT"
WEB_APPLICATION_URL = "WEB_APPLICATION_URL"
WEB_APPLICATION_TITLE = "WEB_APPLICATION_TITLE"
USE_WEB_APPLICATION = "USE_WEB_APPLICATION"
USE_PROFILE_DATA = "USE_PROFILE_DATA"

USE_CALENDAR_EXTENSION = "USE_CALENDAR_EXTENSION"
DEFAULT_CALENDAR = "DEFAULT_CALENDAR"

WITH_FLAT = "WITH_FLAT"
WITH_COMMENT = "WITH_COMMENT"
WITH_PORCH = "WITH_PORCH"
WITH_STREET = "WITH_STREET"

USE_CALLS_OFFICE = "USE_CALLS_OFFICE"
USE_CALLS_DRIVER = "USE_CALLS_DRIVER"
USE_CALLS = "USE_CALLS"

LANGUAGES = "LANGUAGES"

PHOTO_TYPE = "PHOTO_TYPE"
USE_PHOTO = "USE_PHOTO"

USE_ORDER_TIME = "USE_ORDER_TIME"
USE_WISHES = "USE_WISHES"
USE_ADDRESS_DETAIL = "USE_ADDRESS_DETAIL"
DEFAULT_LANGUAGE = "DEFAULT_LANG"

WITH_SHOW_CARS = "WITH_SHOW_CAR"
CAR_RADIUS = "CAR_RADIUS"
USE_MULTI_CALLCOST = "USE_MULTI_CALLCOST"
IS_LET_REJECT_AFTER_ASSIGNED = "IS_LET_REJECT_AFTER_ASSIGNED"
USE_COURIER_FORM = "USE_COURIER_FORM"

PAYMENT_WITH_CASH = "PAYMENT_WITH_CASH"
SHOW_COMPANY_BALANCE = "SHOW_COMPANY_BALANCE"
PAYMENT_WITH_CARDS = "PAYMENT_WITH_CARDS"
PAYMENT_WITH_BONUS = "PAYMENT_WITH_BONUS"
PAYMENT_WITH_COMPANY = "PAYMENT_WITH_COMPANY"
PAYMENT_WITH_PERSONAL = "PAYMENT_WITH_PERSONAL"

MAPS = "MAPS"
DEFAULT_MAP = "DEFAULT_MAP"


# Constant types
# Photo types
CAR_TYPE = "CAR_PHOTO"
DRIVER_TYPE = "DRIVER_PHOTO"


class AndroidConfigurator:

    def __init__(self, file_path):
        self.file_path = file_path


    # FIND REGEX
    @staticmethod
    def regex_psfs(key):
        return '^.*\s' + key + '\s=\s\"([^\"]+)\".*$'


    @staticmethod
    def regex_obj(key):
        return '^.*\s' + key + '\s*=\s*([^;]+).*$'


    # FIND FUNCTIONS
    def find_psfs(self, text, key):
        return re.findall(self.regex_psfs(key), text, flags=re.MULTILINE)


    def find_obj(self, text, key):
        return re.findall(self.regex_obj(key), text, flags=re.MULTILINE)


    # PUT FUNCTIONS
    def put_string(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_psfs(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new)), end='')
                else:
                    print(line, end='')


    def put_obj(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_obj(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new)), end='')
                else:
                    print(line, end='')


    def put_bool(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_obj(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new).lower()), end='')
                else:
                    print(line, end='')


    @staticmethod
    def convert_type_photo(photo_type):
        type_car = "car"
        type_driver = "driver"

        if photo_type == type_car:
            return CAR_TYPE
        if photo_type == type_driver:
            return DRIVER_TYPE
        return CAR_TYPE

    @staticmethod
    def convert_calendar(calendar):
        if calendar == 'gregorian':
            return 0
        if calendar == 'persian':
            return 1
        return 0


    # CONFIGURABLE BY APPLICATION
    def configure_by_app(self, config: app.Application):
        self.configure_calls(config)
        self.configure_photo(config)
        self.configure_order_panel(config)
        self.configure_address(config)
        self.configure_calendar(config)
        self.configure_default(config)
        self.configure_params(config)
        self.configure_payment(config)
        self.configure_map(config)


    def configure_calls(self, config):
        self.put_bool(USE_CALLS_OFFICE, config.use_calls_office)
        self.put_bool(USE_CALLS, config.use_calls)
        self.put_bool(USE_CALLS_DRIVER, config.use_calls_driver)


    def configure_photo(self, config):
        self.put_bool(USE_PHOTO, config.use_photo)
        photo_type = self.convert_type_photo(config.photo_type)
        self.put_obj(PHOTO_TYPE, photo_type)


    def configure_order_panel(self, config):
        self.put_bool(USE_ORDER_TIME, config.use_pre_orders)
        self.put_bool(USE_WISHES, config.use_wishes)
        self.put_bool(USE_ADDRESS_DETAIL, config.use_detail)


    def configure_address(self, config):
        self.put_bool(WITH_FLAT, config.use_flat)
        self.put_bool(WITH_COMMENT, config.use_comment)
        self.put_bool(WITH_PORCH, config.use_porch)
        self.put_bool(WITH_STREET, config.use_street)


    def configure_calendar(self, config):
        self.put_bool(USE_CALENDAR_EXTENSION, config.use_calendars)
        calendar = self.convert_calendar(config.default_calendar)
        self.put_obj(DEFAULT_CALENDAR, calendar)


    def configure_default(self, config):
        self.put_bool(IS_DEMO, config.is_demo)
        self.put_bool(FILL_SPLASH, config.is_full_splash)
        self.put_bool(USE_REFERRAL, config.use_referral)
        self.put_bool(USE_REVIEW_BLOCK, config.use_review_block)
        self.put_bool(WITH_COUNTRY, config.use_country)
        self.put_bool(ORDER_WITH_ONE_ADDRESS, config.use_one_address)
        self.put_bool(WITH_MAX_ONE_ADDRESS, config.max_one_address)
        self.put_bool(USE_SEARCH, config.use_search)
        self.put_bool(WITH_EDIT_ORDER, config.with_edit_order)
        self.put_string(AUTOCOMPLETE_RADIUS, config.autocomplete)
        self.put_string(REVERSE_RADIUS, config.reverse_radius)
        self.put_bool(SHOWN_CLIENT_ID, config.shown_client_id)
        self.put_bool(USE_REVIEW_DETAIL, config.use_review_detail)
        self.put_bool(USE_REVIEW_FOR_REJECTED, config.use_review_for_rejected)

        self.put_bool(USE_PUBLIC_TRANSPORT, config.use_public_transport)
        self.put_bool(USE_WEB_APPLICATION, config.use_web_application)
        self.put_string(WEB_APPLICATION_URL, config.web_application_url)
        self.put_string(WEB_APPLICATION_TITLE, config.web_application_title)
        self.put_bool(USE_PROFILE_DATA, config.use_profile_data)
        self.put_bool(IS_LET_REJECT_AFTER_ASSIGNED, config.is_let_reject_after_assigned)


    def configure_params(self, config):
        self.put_string(TENANT_ID, config.tenant_id)
        self.put_string(APP_ID, config.app_id)
        self.put_string(API_KEY, config.api_key)
        self.put_string(PUSH_SENDER_ID, config.push_key)
        self.put_string(METRICA_KEY, config.metrica_key)
        self.put_string(URL, config.client_url)
        self.put_string(GEO_URL, config.geo_url)
        self.put_obj(LANGUAGES, config.lang)
        self.put_string(DEFAULT_LANGUAGE, config.default_language.lower())

        self.put_string(CAR_RADIUS, config.car_radius)
        self.put_bool(WITH_SHOW_CARS, config.with_show_cars)
        self.put_bool(USE_MULTI_CALLCOST, config.use_multi_callcost)
        self.put_bool(USE_COURIER_FORM, config.use_courier_form)


    def configure_payment(self, config):
        self.put_bool(PAYMENT_WITH_CARDS, config.use_payment_card)
        self.put_bool(PAYMENT_WITH_CASH, config.use_payment_cash)
        self.put_bool(PAYMENT_WITH_COMPANY, config.use_payment_corp)
        self.put_bool(PAYMENT_WITH_BONUS, config.use_payment_bonus)
        self.put_bool(PAYMENT_WITH_PERSONAL, config.use_payment_personal)
        self.put_bool(SHOW_COMPANY_BALANCE, config.show_company_balance)


    def configure_map(self, config):
        result = []

        if config.use_google:
            result.append(1)

        if config.use_google_hybrid:
            result.append(2)

        if config.use_yandex_map:
            result.append(3)

        if config.use_gis_map:
            result.append(4)

        result = str(result).replace("[", "{").replace("]", "}")
        self.put_obj(MAPS, result)

        def_map = config.default_map
        if def_map == 'google':
            self.put_obj(DEFAULT_MAP, 1)
        elif def_map == 'google_hybrid':
            self.put_obj(DEFAULT_MAP, 2)
        elif def_map == 'yandex':
            self.put_obj(DEFAULT_MAP, 3)
        elif def_map == 'gis':
            self.put_obj(DEFAULT_MAP, 4)

