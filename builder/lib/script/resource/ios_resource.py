import shutil
import re
import xml.etree.ElementTree as ET

from flask import json

from std.std import merge


SCALE_LIST = ["@2", "@3"]
RES_PATH = "Client/Assets.xcassets"

CONTENT = "Contents.json"
CONTENT_APP = "ContentsApp.json"
CONTENT_LAUNCH_IMAGE = "ContentLaunchImange.json"
LAUNCH_IMAGE = "LaunchImage"

imageset = '.imageset'
launchimage = '.launchimage'
appiconset = '.appiconset'
res_type = 'ios'
png = ".png"

idiom_iphone = "iphone"
idiom_ipad = "ipad"


# TODO REPLACE FUNCTIONAL FOR FUNCTIONS (REPLACE JSON ON GENERATE JSON)
class IosResourceHelper:
    def __init__(self, assets_ios, path_to_res, finish_path):
        self.assets_path = assets_ios
        self.path_to_res = path_to_res
        self.finish_path = finish_path
        self.plist_path = merge(self.finish_path, "/Client/Info.plist")


    # Create Content.json for IMAGE-SET
    def __create_set_content(self, name):
        scale = "scale"
        images = "images"
        filename = "filename"
        content = "Contents.json"
        SCALES = {"2x": "@2", "3x": "@3"}

        content_path = merge(self.assets_path, content)

        with open(content_path) as data_file:
            content_json = json.load(data_file)
        for image in content_json[images]:
            for scale_key in SCALES.keys():
                if image[scale] == scale_key:
                    image[filename] = name + SCALES[scale_key] + png

        file = open(merge(self.finish_path, RES_PATH, name + imageset, content), 'w+')
        file.write(json.dumps(content_json))
        file.close()


    # Create Content.json for LOGO-SET
    def __create_logo_content(self, name):
        itunnes = "itunesartwork@2x"

        scale = "scale"
        images = "images"
        filename = "filename"
        idiom = "idiom"
        size = "size"

        IPHONE_SCALES = {"2x": "@2", "3x": "@3"}
        IPHONE_SIZES = ["20x20", "29x29", "40x40", "60x60"]

        IPOD_SCALES = {"1x": "@1", "2x": "@2"}
        IPOD_SIZES = ["20x20", "29x29", "40x40", "60x60", "76x76", "83.5x83.5"]

        content_path = merge(self.assets_path, CONTENT_APP)

        with open(content_path) as data_file:
            content_json = json.load(data_file)  # TODO

        # TODO GOVNOCODE
        for image in content_json[images]:
            if image[idiom] == idiom_iphone:
                for iphone_size in IPHONE_SIZES:
                    if iphone_size == image[size]:
                        for scale_key in IPHONE_SCALES.keys():
                            if image[scale] == scale_key:
                                # logo_iphone20x20@2.png
                                image[filename] = name + "-" + idiom_iphone + iphone_size + IPHONE_SCALES[
                                    scale_key] + png
            if image[idiom] == idiom_ipad:
                for ipod_size in IPOD_SIZES:
                    if ipod_size == image[size]:
                        for scale_key in IPOD_SCALES.keys():
                            if image[scale] == scale_key:
                                # logo_ipad20x20@1.png
                                image[filename] = name + "-" + idiom_ipad + ipod_size + IPOD_SCALES[scale_key] + png

        file = open(merge(self.finish_path, RES_PATH, name + appiconset, CONTENT), 'w+')
        file.write(json.dumps(content_json))
        file.close()


    # Replace logo_splash images and create image set
    def replace_image_set(self, image_name):
        self.remove_images_content(merge(self.finish_path, RES_PATH, image_name + imageset))

        for scale in SCALE_LIST:
            shutil.copy(src=merge(self.path_to_res, res_type, image_name, image_name + scale + png),
                        dst=merge(self.finish_path, RES_PATH, image_name + imageset, image_name + scale + png))

        self.__create_set_content(image_name)


    def __create_launch_image_content(self):
        launch_content_path = merge(self.assets_path, CONTENT_LAUNCH_IMAGE)
        destination_path = merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, CONTENT)

        shutil.copy(src=merge(launch_content_path),
                    dst=merge(destination_path))


    def replace_launch_image(self, image_name):
        IDIOMS = ["iphone", "ipad"]

        SIZE_IPHONE_1242x2208 = "1242x2208"
        SIZE_IPHONE_750x1334 = "750x1334"
        SIZE_IPHONE_640x960 = "640x960"
        SIZE_IPHONE_640x1136 = "640x1136"
        SIZE_IPAD_768x1024 = "1024x768"
        SIZE_IPAD_1536x2048 = "2048x1536"
        SIZE_IPAD_1125x2436 = "1125x2436"

        for idiom in IDIOMS:
            if idiom is idiom_iphone:
                # 1242x2208
                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_1242x2208 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPHONE_1242x2208 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_750x1334 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPHONE_750x1334 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_640x960 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPHONE_640x960 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_640x1136 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPHONE_640x1136 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPAD_1125x2436 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPAD_1125x2436 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_640x1136 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage,
                              SIZE_IPHONE_640x1136 + "-1" + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPHONE_640x960 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPHONE_640x960 + "-1" + png))

            if idiom is idiom_ipad:
                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPAD_768x1024 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPAD_768x1024 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPAD_1536x2048 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPAD_1536x2048 + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPAD_768x1024 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPAD_768x1024 + "-1" + png))

                shutil.copy(
                    src=merge(self.path_to_res, res_type, image_name, SIZE_IPAD_1536x2048 + png),
                    dst=merge(self.finish_path, RES_PATH, LAUNCH_IMAGE + launchimage, SIZE_IPAD_1536x2048 + "-1" + png))


    # Replace logo_splash images and create logo set
    def replace_logo(self):
        logo = "appicon"
        itunnes = "itunesartwork@2x"

        IDIOMS = ["iphone", "ipad"]

        idiom_iphone = "iphone"
        IPHONE_SCALES = ["@2", "@3"]
        IPHONE_SIZES = ["20x20", "29x29", "40x40", "60x60"]

        idiom_ipad = "ipad"
        IPAD_SIZES = ["20x20", "29x29", "40x40", "76x76", "83.5x83.5"]  # TODO
        IPAD_SCALES = ["@1", "@2"]

        self.remove_images_content(merge(self.finish_path, RES_PATH, logo + appiconset))

        # TODO GOVNOCODE
        for idiom in IDIOMS:
            if idiom == idiom_iphone:
                for size in IPHONE_SIZES:
                    for scale in IPHONE_SCALES:
                        shutil.copy(
                            src=merge(self.path_to_res, res_type, logo, logo + "-" + idiom_iphone + size + scale + png),
                            # TODO
                            dst=merge(self.finish_path, RES_PATH, logo + appiconset,
                                      logo + "-" + idiom_iphone + size + scale + png))
            if idiom == idiom_ipad:
                for size in IPAD_SIZES:
                    for scale in IPAD_SCALES:
                        shutil.copy(
                            src=merge(self.path_to_res, res_type, logo, logo + "-" + idiom_ipad + size + scale + png),
                            # TODO
                            dst=merge(self.finish_path, RES_PATH, logo + appiconset,
                                      logo + "-" + idiom_ipad + size + scale + png))

        self.__create_logo_content(logo)


    @staticmethod
    def replace_colors(screen_path, splash_color):
        from std.helper import math_color

        tree = ET.parse(screen_path)
        root = tree.getroot()

        for color in root.iter('color'):
            colors = math_color.get_double_colors(splash_color)
            color.attrib[math_color.RED] = str(colors[math_color.RED])
            color.attrib[math_color.GREEN] = str(colors[math_color.GREEN])
            color.attrib[math_color.BLUE] = str(colors[math_color.BLUE])

        tree.write(screen_path)


    @staticmethod
    def remove_images_content(folder):
        import os
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


    def replace_project_name(self, name):
        tree = ET.parse(self.plist_path)
        root = tree.getroot()
        plist_dict = root.find("dict")

        for index, item in enumerate(plist_dict):
            if item.text == "CFBundleDisplayName":
                plist_dict[index + 1].text = name
        tree.write(self.plist_path)


    def replace_short_version(self, version: str):
        tree = ET.parse(self.plist_path)
        root = tree.getroot()
        plist_dict = root.find("dict")

        for index, item in enumerate(plist_dict):
            if item.text == "CFBundleShortVersionString":
                plist_dict[index + 1].text = version
        tree.write(self.plist_path)


    def replace_version(self, version: str):
        tree = ET.parse(self.plist_path)
        root = tree.getroot()
        plist_dict = root.find("dict")

        for index, item in enumerate(plist_dict):
            if item.text == "CFBundleVersion":
                plist_dict[index + 1].text = version
        tree.write(self.plist_path)


    @staticmethod
    def regex_array_item(key):
        return '^.*\s' + key + '\s*=\s*\[\[(.*)],.*'


    @staticmethod
    def parse_array(colors: str):
        return colors.replace("{", "").replace("}", "")


    def find_array_item(self, text, key):
        return re.findall(self.regex_array_item(key), text, flags=re.MULTILINE)


    # PUT FUNCTIONS
    def put_color_scheme(self, file_path, theme_json):
        new = self.parse_array(theme_json)
        print(theme_json)
        with open(file_path) as file:
            file_content = file.read()
            group = self.find_array_item(file_content, "schemes")
            print(group)
            if len(group) > 0:
                content = file_content.replace(group[0], str(new))
            else:
                content = file_content
        file = open(file_path, 'w+')
        file.write(content)
        file.close()
