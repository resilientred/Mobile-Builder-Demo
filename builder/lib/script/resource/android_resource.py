import shutil
import xml.etree.ElementTree as ET

from backend.util.manager.asset_man import country_name_en, country_name_ru
from std.std import merge
from std.config import COUNTRY_LIST, COUNTRY_DRIVER_LIST


DPI_LIST = ["-mdpi", "-hdpi", "-xhdpi", "-xxhdpi"]
RES_PATH = "/app/src/main/res"

THEME_FIELDS = ["splash_bg", "accent_bg", "accent_text", "menu_bg", "menu_text", "menu_stroke", "content_bg",
                "content_text", "content_stroke", "content_icon_bg", "content_icon_stroke", "map_marker_bg",
                "map_marker_bg_stroke", "map_marker_text", "map_car_bg", "accent_bg_tariff"]


class AndroidResourceHelper:

    def __init__(self, path_to_res, final_path):
        self.path_to_res = path_to_res
        self.finish_path = final_path


    def replace_google_driver_service(self):
        res_type = 'google_driver'
        google_services = "/google-services.json"

        shutil.copy(src=merge(self.path_to_res, res_type, google_services),
                    dst=merge(self.finish_path, "/app", google_services))

    # REPLACE PROJECT METHODS
    def replace_mipmap(self, name):
        res_type = 'android_driver'
        mipmap = "/mipmap"
        logo = f"/{name}"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, logo, logo + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, mipmap + dpi, logo + png))

    def replace_drawable(self, name):
        res_type = 'android_driver'
        drawable = "/drawable"
        splash = f"/{name}"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, splash, splash + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, drawable + dpi, splash + png))

    def replace_logo(self):
        res_type = 'android'
        mipmap = "/mipmap"
        logo = "/logo"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, logo, logo + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, mipmap + dpi, logo + png))


    def replace_splash(self):
        res_type = 'android'
        drawable = "/drawable"
        splash = "/splash"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, splash, splash + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, drawable + dpi, splash + png))


    def replace_push(self):
        res_type = 'android'
        drawable = "/drawable"
        push = "/push"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, push, push + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, drawable + dpi, push + png))


    def replace_cars(self):
        res_type = 'android'
        drawable = "/drawable"
        car = "/car"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, car, car + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, drawable + dpi, car + png))


    def replace_menulogo(self):
        res_type = 'android'
        drawable = "/drawable"
        menulogo = "/menulogo"
        png = ".png"

        for dpi in DPI_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, menulogo, menulogo + dpi + png),
                        dst=merge(self.finish_path, RES_PATH, drawable + dpi, menulogo + png))


    def replace_google_service(self):
        res_type = 'google'
        google_services = "/google-services.json"

        shutil.copy(src=merge(self.path_to_res, res_type, google_services),
                    dst=merge(self.finish_path, "/app", google_services))


    def replace_phone(self, new_phone):
        values = "/values"
        strings = "/strings.xml"

        string_tag = "string"
        name_tag = "name"
        phone_auth_tag = "activities.AuthActivity.edit_phone_mask"
        phone_profile_tag = "activities.ProfileActivity.phone_default"

        for country in COUNTRY_LIST:
            file_path = merge(self.finish_path, RES_PATH, values + country, strings)

            tree = ET.parse(file_path)
            root = tree.getroot()

            for name in root.findall(string_tag):
                tag = name.get(name_tag)
                if tag == phone_auth_tag or tag == phone_profile_tag:
                    name.text = new_phone
            tree.write(file_path)


    def replace_country(self, new_country):
        values = "/values"
        strings = "/strings.xml"

        string_tag = "string"
        name_tag = "name"
        country_tag = "activities.AuthActivity.edit_country"

        for country in COUNTRY_LIST:
            file_path = merge(self.finish_path, RES_PATH, values + country, strings)
            tree = ET.parse(file_path)
            root = tree.getroot()

            for name in root.findall(string_tag):
                if name.get(name_tag) == country_tag:
                    if country == "-ru":
                        name.text = new_country[country_name_ru]
                    else:
                        name.text = new_country[country_name_en]
            tree.write(file_path)


    def replace_app_name(self, new_name, type="client"):
        string_tag = "string"
        name_tag = "name"
        app_name_tag = "app_name"
        values = "/values"
        strings = "/strings.xml"

        if type == "client":
            counties = COUNTRY_LIST
        else:
            counties = COUNTRY_DRIVER_LIST

        for country in counties:
            file_path = merge(self.finish_path, RES_PATH, values + country, strings)
            tree = ET.parse(file_path)
            root = tree.getroot()

            for name in root.findall(string_tag):
                if name.get(name_tag) == app_name_tag:
                    name.text = new_name
            tree.write(file_path)


    def replace_colors(self, theme: dict):
        values = "/values"
        colors = "/colors.xml"

        color_tag = "color"
        name_tag = "name"

        file_path = merge(self.finish_path, RES_PATH, values, colors)

        tree = ET.parse(file_path)
        root = tree.getroot()

        for line in root.findall(color_tag):
            for attr in THEME_FIELDS:
                if line.get(name_tag) == attr:
                    line.text = theme[attr]
        tree.write(file_path)


    def replace_google_key(self, google_key):
        # This variables is static, not changing never
        google_map_key = "com.google.android.maps.v2.API_KEY"
        manifest_path = "/app/src/main/AndroidManifest.xml"

        print(f"Google key123 {google_key}")
        namespace_key_android = "android"
        namespace_value_android = "http://schemas.android.com/apk/res/android"

        meta_data_value = "{" + namespace_value_android + "}value"
        meta_data = 'meta-data'

        tree = ET.parse(self.finish_path + manifest_path)
        ET.register_namespace(namespace_key_android, namespace_value_android)
        root = tree.getroot()
        application = root.find("application")

        for meta in application.iter(meta_data):
            if google_map_key in str(meta.attrib):
                print(f"Google key {google_key}")
                meta.set(meta_data_value, google_key)

        tree.write(self.finish_path + manifest_path)


    def replace_google_key_driver(self, google_key):
        # This variables is static, not changing never
        google_map_key = "com.google.android.geo.API_KEY"
        manifest_path = "/app/src/main/AndroidManifest.xml"

        print(f"Google key123 {google_key}")
        namespace_key_android = "android"
        namespace_value_android = "http://schemas.android.com/apk/res/android"

        meta_data_value = "{" + namespace_value_android + "}value"
        meta_data = 'meta-data'

        tree = ET.parse(self.finish_path + manifest_path)
        ET.register_namespace(namespace_key_android, namespace_value_android)
        root = tree.getroot()
        application = root.find("application")

        for meta in application.iter(meta_data):
            if google_map_key in str(meta.attrib):
                print(f"Google key {google_key}")
                meta.set(meta_data_value, google_key)

        tree.write(self.finish_path + manifest_path)