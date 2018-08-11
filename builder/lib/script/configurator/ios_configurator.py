import fileinput
import re

from backend.model.entity import app


# This class parse and replace value in AppParams by key
TENANT_ID = "gxDefTenantID"
API_KEY = "gxSecretKey"
GOOGLE_MAP_KEY = "googleMapKey"
APP_ID = "appId"
METRICA_KEY = "yandexMetricaAPIkey"
URL = "baseUrl"
GEO_URL = "geoUrl"

IS_DEMO = "isDemo"
USE_REFERRAL = "allowReferralSystem"
USE_REVIEW_BLOCK = "useReviewBlock"
WITH_COUNTRY = "withCountry"
WITH_EDIT_ORDER = "allowEditOrder"

USE_SEARCH = "useSearch"
SEARCH_RADIUS = "searchRadius"
ORDER_WITH_ONE_ADDRESS = "orderWithOnePoint"
WITH_MAX_ONE_ADDRESS = "maxOnePoint"
SHOWN_CLIENT_ID = "isShowClientId"
USE_REVIEW_DETAIL = "useReviewDetail"
USE_REVIEW_FOR_REJECTED = "useReviewForRejected"
USE_PROFILE_DATA = "useProfileData"

USE_CALENDAR_EXTENSION = "useCalendarExtensions"
DEFAULT_CALENDAR = "defaultCalendar"

WITH_FLAT = "needFlat"
WITH_COMMENT = "needComment"
WITH_PORCH = "needPorch"
WITH_STREET = "needStreet"

USE_CALLS_OFFICE = "needOfficeCall"
USE_CALLS_DRIVER = "needDriverCall"
USE_CALLS = "useCalls"

LANGUAGES = "languages"

PHOTO_TYPE = "photoType"
USE_PHOTO = "usePhoto"

USE_ORDER_TIME = "needPreOrder"
USE_WISHES = "needWishes"
USE_ADDRESS_DETAIL = "needAddressDetail"
USE_MULTI_CALLCOST = "allowTariffCallCost"

PAYMENT_WITH_CASH = "allowPaymentInCash"
SHOW_COMPANY_BALANCE = "allowPaymentInCompany"
PAYMENT_WITH_CARDS = "allowAddingCreditCard"
PAYMENT_WITH_BONUS = "allowPaymentInBonus"
PAYMENT_WITH_PERSONAL = "allowPaymentInPerosnal"
PAYMENT_WITH_COMPANY = "allowPaymentInCompany"

USE_GOOGLE_MAP = "needGoogleMapNormal"
USE_GOOGLE_HYBRID_MAP = "needGoogleMapHybrid"
USE_OSM_MAP = "needOSMMap"
USE_2GIS_MAP = "needGisMap"
DEFAULT_MAP = "defaultMap"
CURRENT_MAPS = "currentMaps"
DEFAULT_GOOGLE_TYPE = "defaultGoogleType"
DEFAULT_LANGUAGE = "defaultLanguage"
IS_LET_REJECT_AFTER_ASSIGNED = "letRejectAfterAssigned"
USE_COURIER_FORM = "useCourierForm"

# Constant types
# Photo types
CAR_TYPE = "carPhoto"
DRIVER_TYPE = "driverPhoto"

USE_WEB_SCREEN = "useWebScreen"
WEB_SCREEN_TITLE = "webScreenTitle"
WEB_SCREEN_URL = "webScreenUrl"
USE_PUBLIC_TRANSPORT = "allowPublicTransport"

WITH_SHOW_CARS = "withShowCars"
CAR_RADIUS = "carRadius"


class IosConfigurator:
    def __init__(self, file_path, constant_path):
        self.file_path = file_path
        self.constant_path = constant_path


    # FIND REGEX
    @staticmethod
    def regex_psfs(key):
        return '^.*\s' + key + '\s=\s\"([^\"]+)\".*$'


    @staticmethod
    def regex_obj(key):
        return '^.*\s' + key + '\s*=\s*([^;]+).*$'


    @staticmethod
    def parse_array(colors: str):
        return colors.replace("{", "[").replace("}", "]").replace("av", "uz-Latn")


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
                    print(line.replace(group[0], str(new)), end='\n')
                else:
                    print(line, end='')


    def put_bool(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_obj(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new).lower()), end='\n')
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
        self.configure_language(config)


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
        self.put_bool(USE_REFERRAL, config.use_referral)
        self.put_bool(USE_REVIEW_BLOCK, config.use_review_block)
        self.put_bool(WITH_COUNTRY, config.use_country)
        self.put_bool(ORDER_WITH_ONE_ADDRESS, config.use_one_address)
        self.put_bool(WITH_MAX_ONE_ADDRESS, config.max_one_address)
        self.put_bool(USE_SEARCH, config.use_search)
        self.put_bool(SHOWN_CLIENT_ID, config.shown_client_id)
        self.put_bool(USE_REVIEW_DETAIL, config.use_review_detail)
        self.put_bool(WITH_EDIT_ORDER, config.with_edit_order)
        self.put_bool(USE_REVIEW_FOR_REJECTED, config.use_review_for_rejected)
        self.put_string(SEARCH_RADIUS, config.autocomplete)
        self.put_string(GOOGLE_MAP_KEY, config.google_map_ios)
        self.put_bool(USE_PROFILE_DATA, config.use_profile_data)

        self.put_string(WEB_SCREEN_URL, config.web_application_url)
        self.put_string(WEB_SCREEN_TITLE, config.web_application_title)
        self.put_bool(USE_WEB_SCREEN, config.use_web_application)
        self.put_bool(USE_PUBLIC_TRANSPORT, config.use_public_transport)
        self.put_bool(USE_MULTI_CALLCOST, config.use_multi_callcost)

        self.put_bool(WITH_SHOW_CARS, config.with_show_cars)
        self.put_string(CAR_RADIUS, config.car_radius)
        self.put_bool(USE_COURIER_FORM, config.use_courier_form)


    def configure_params(self, config):
        self.put_string(TENANT_ID, config.tenant_id)
        self.put_string(APP_ID, config.app_id)
        self.put_string(API_KEY, config.api_key)
        self.put_string(METRICA_KEY, config.metrica_key)
        self.put_obj(LANGUAGES, self.parse_array(config.lang))

        url = config.client_url + "/"
        self.put_string(URL, url)

        geo_url = config.geo_url + "/"
        self.put_string(GEO_URL, geo_url)


    def configure_payment(self, config):
        self.put_bool(PAYMENT_WITH_CARDS, config.use_payment_card)
        self.put_bool(PAYMENT_WITH_CASH, config.use_payment_cash)
        self.put_bool(PAYMENT_WITH_COMPANY, config.use_payment_corp)
        self.put_bool(PAYMENT_WITH_BONUS, config.use_payment_bonus)
        self.put_bool(SHOW_COMPANY_BALANCE, config.show_company_balance)
        self.put_bool(PAYMENT_WITH_PERSONAL, config.use_payment_personal)
        self.put_bool(IS_LET_REJECT_AFTER_ASSIGNED, config.is_let_reject_after_assigned)


    def configure_map(self, config):
        result = []

        if config.use_osm_map:
            result.append(0)

        if config.use_google:
            result.append(1)

        if config.use_google_hybrid:
            result.append(2)

        if config.use_gis_map:
            result.append(3)

        result = str(result)
        self.put_obj(CURRENT_MAPS, result)

        def_map = config.default_map
        if def_map == 'google':
            self.put_obj(DEFAULT_MAP, 1)
        elif def_map == 'google_hybrid':
            self.put_obj(DEFAULT_MAP, 2)
        elif def_map == 'osm':
            self.put_obj(DEFAULT_MAP, 0)



    @staticmethod
    def regex_language():
        return '^.*\sarr\.append\(([^;]+)\)$'


    def find_language(self, text):
        return re.findall(self.regex_language(), text, flags=re.MULTILINE)


    # PUT FUNCTIONS
    def find_language_line(self, key) -> str:
        language_block = ""
        with fileinput.FileInput(self.constant_path, inplace=True) as file:
            for line in file:
                if f"country.{key}" in str(line):
                    matches = self.find_language(line)
                    if len(matches) > 0:
                        language_block = matches[0]
                print(line, end='')
        return language_block


    # FIND REGEX
    @staticmethod
    def regex_return():
        return '^.*\sreturn\s{1}([^;]+)$'


    # FIND FUNCTIONS
    def find_return(self, text):
        return re.findall(self.regex_return(), text, flags=re.MULTILINE)


    def put_return(self, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_return(line)
                if len(group) > 0:
                    print(line.replace(group[0], str(new)), end='\n')
                else:
                    print(line, end='')


    def configure_language(self, config):
        self.put_string(DEFAULT_LANGUAGE, config.default_language.lower())
        print(f"Default language {config.default_language}")
        lang_block = self.find_language_line(str(config.country).lower())
        print(f"Country black {lang_block}")
        if len(lang_block) > 0:
            self.put_return(lang_block)

