import logging
import os
import traceback

from backend.model.helper.app_helper import parse_sku
from std import stdres as res
from std.disk.disk import Disk
from std.disk.google_disk import GoogleDisk
from std.error.base_error import BaseError
from std.error.res_error import ResourceError
from std.std import merge


# Types mode
create = 'create'
update = 'update'

ANDROID = "android"
IOS = "ios"
GOOGLE = "google"
ICON = "icon"

ANDROID_DRIVER = "android_driver"
GOOGLE_DRIVER = "google_driver"


class ResourceManager:

    def __init__(self, res_path: str, temp_path: str):
        self.res_path = res_path
        self.temp_path = temp_path


    def generate_new_res(self, name: str) -> None:
        if not res.name_exist(self.res_path, name):
            res.create(self.res_path, name)
        else:
            raise ResourceError(subcode=ResourceError.res_exist,
                                data=ResourceError.res_not_found_mes % name)


    def update_res(self, old: str, new: str) -> None:
        if old != new:
            if res.name_exist(self.res_path, old):
                if not res.name_exist(self.res_path, new):
                    res.update(self.res_path, old, new)
                else:
                    raise ResourceError(subcode=ResourceError.res_exist,
                                        data=ResourceError.res_exist_mes % new)
            else:
                raise ResourceError(subcode=ResourceError.res_not_found,
                                    data=ResourceError.res_not_found_mes % old)


    @staticmethod
    def generate_new_type(path_to_res: str, res_type: str) -> None:
        if not res.validate_type(path_to_res, res_type):
            res.create(path_to_res, res_type)


    def generate_zip_res(self, file, name: str, res_type: str) -> None:
        path_temp_res = merge(self.temp_path, name)
        path_temp_type = merge(self.temp_path, name, res_type)
        path_res_type = merge(self.res_path, name, res_type)
        zip_name = name + "-" + res_type + ".zip"

        if res.allowed_zip(file.filename):
            res.unzip_temp(file, zip_name, path_temp_res, res_type)
            try:
                # Validation and store files
                self.validate_res_by_type(res_type, path_temp_type)
                if res_type == IOS:
                    from std.migration import ios_image_migrate
                    try:
                        ios_image_migrate.create_logo_content(path_temp_type, path_res_type)
                    except Exception:
                        raise ResourceError(subcode=ResourceError.res_not_found,
                                            data=ResourceError.ios_image_res)
                elif res_type == ANDROID:
                    res.save_temp(path_temp_type, path_res_type)
                elif res_type == ANDROID_DRIVER:
                    print("generate_zip_res")
                    res.save_temp(path_temp_type, path_res_type)
                else:
                    raise ResourceError(subcode=ResourceError.res_not_found,
                                        data=ResourceError.res_not_found_mes % res_type)

                # Create ZIP for Google
                path = merge(path_temp_res, parse_sku(name) + "-" + res_type)
                res.create_zip_res(path_res_type, path)

                # Load to Google
                gzip_name = parse_sku(name) + "-" + res_type + ".zip"
                gzip_path = merge(path_temp_res, gzip_name)
                disk: Disk = GoogleDisk(with_auth=True)
                disk.replace_file(gzip_path, gzip_name, disk.get_folder_id_by_name(name))

                # Delete temp
                res.delete(path_temp_res)
            except ResourceError as error:
                # res.delete(path_temp_res)
                raise error
        else:
            raise ResourceError(subcode=ResourceError.file_type,
                                data=ResourceError.file_type_mes % (file.filename, "zip"))


    def generate_google_res(self, file, name: str) -> None:

        temp_res = merge(self.temp_path, name)
        path_res_temp = merge(self.temp_path, name, GOOGLE)
        path_to_type = merge(self.res_path, name, GOOGLE)

        json_name = "google-services.json"
        json_path = merge(path_res_temp, json_name)

        if res.allowed_json(file.filename):
            res.save_json(file, path_res_temp)
            if self.validate_res_by_type(GOOGLE, path_res_temp):
                res.save_temp(path_res_temp, path_to_type)

                disk: GoogleDisk = GoogleDisk(with_auth=True)
                disk.replace_file(json_path, json_name, disk.get_folder_id_by_name(name))

                res.delete(temp_res)
            else:
                res.delete(temp_res)
                raise ResourceError(subcode=ResourceError.google_res,
                                    data=ResourceError.google_res_mes % "not file")
        else:
            raise ResourceError(subcode=ResourceError.file_type,
                                data=ResourceError.file_type_mes % (file.filename, "json"))

    def generate_driver_google_res(self, file, name: str) -> None:

        temp_res = merge(self.temp_path, name)
        path_res_temp = merge(self.temp_path, name, GOOGLE_DRIVER)
        path_to_type = merge(self.res_path, name, GOOGLE_DRIVER)

        json_name = "google-services.json"
        json_path = merge(path_res_temp, json_name)

        if res.allowed_json(file.filename):
            res.save_json(file, path_res_temp)
            if self.validate_res_by_type(GOOGLE_DRIVER, path_res_temp):
                res.save_temp(path_res_temp, path_to_type)

                disk: GoogleDisk = GoogleDisk(with_auth=True)
                disk.replace_file(json_path, json_name, disk.get_folder_id_by_name(name))

                res.delete(temp_res)
            else:
                res.delete(temp_res)
                raise ResourceError(subcode=ResourceError.google_res,
                                    data=ResourceError.google_res_mes % "not file")
        else:
            raise ResourceError(subcode=ResourceError.file_type,
                                data=ResourceError.file_type_mes % (file.filename, "json"))


    @staticmethod
    def create_app_icon(files, path_to_static: str, bundle: str):
        if ICON in files and files[ICON].filename != '':
            file = files[ICON]
            path_to_type = merge(path_to_static, "apps")

            if not os.path.exists(path_to_type):
                os.makedirs(path_to_type)

            path_bundle = bundle.replace(".", "_")
            path_to_file = merge(path_to_type, path_bundle + ".png")
            file.save(path_to_file)


    @staticmethod
    def validate_res_by_type(res_type: str, path_res_type: str) -> bool:
        if res_type == ANDROID:
            is_valid = res.validate_android_images(path_res_type)
        elif res_type == IOS:
            is_valid = res.validate_ios_images(path_res_type)
        elif res_type == GOOGLE:
            is_valid = res.validate_google_push(path_res_type)
        elif res_type == GOOGLE_DRIVER:
            is_valid = res.validate_google_push(path_res_type)
        elif res_type == ANDROID_DRIVER:
            is_valid = res.validate_driver_images(path_res_type)
        else:
            raise ResourceError(subcode=ResourceError.res_not_found,
                                data=ResourceError.res_not_found_mes % res_type)
        return is_valid


    @staticmethod
    def validate_saved_res_by_type(res_type: str, path_res_type: str) -> bool:
        if res_type == ANDROID:
            is_valid = res.validate_android_images(path_res_type)
        elif res_type == IOS:
            is_valid = res.validate_ios_saved_images(path_res_type)
        elif res_type == GOOGLE:
            is_valid = res.validate_google_push(path_res_type)
        elif res_type == GOOGLE_DRIVER:
            is_valid = res.validate_google_push(path_res_type)
        elif res_type == ANDROID_DRIVER:
            is_valid = res.validate_driver_images(path_res_type)
        else:
            return False
        return is_valid

    def generate_res_files(self, files, name: str):
        logging.info("Files to download " + str(files))

        if files:
            if ANDROID in files and files[ANDROID].filename != '':
                self.generate_zip_res(files[ANDROID], name, ANDROID)
            if GOOGLE_DRIVER in files and files[GOOGLE_DRIVER].filename != '':
                self.generate_driver_google_res(files[GOOGLE_DRIVER], name)
            if GOOGLE in files and files[GOOGLE].filename != '':
                self.generate_google_res(files[GOOGLE], name)
            if IOS in files and files[IOS].filename != '':
                self.generate_zip_res(files[IOS], name, IOS)
            if ANDROID_DRIVER in files and files[ANDROID_DRIVER].filename != '':
                print("GENERATE RED FILES")
                self.generate_zip_res(files[ANDROID_DRIVER], name, ANDROID_DRIVER)


    def validate_resources(self, name: str, with_remote: bool=False) -> dict:
        RES_TYPES = ["google", "android", "ios", "android_driver", "google_driver"]
        result = {}

        path_to_res = merge(self.res_path, name)

        for res_type in RES_TYPES:
            if res.validate_type(path_to_res, res_type):
                try:
                    result[res_type] = ResourceManager.validate_saved_res_by_type(
                        res_type=res_type,
                        path_res_type=merge(path_to_res, res_type)
                    )
                except BaseError:
                    traceback.print_exc()
                    result[res_type] = False
            else:
                result[res_type] = False
            if with_remote and not result[res_type]:
                if res.remote_validate_type(name, res_type, path_to_res, True):
                    try:
                        result[res_type] = ResourceManager.validate_saved_res_by_type(
                            res_type=res_type,
                            path_res_type=merge(path_to_res, res_type)
                        )
                    except BaseError:
                        traceback.print_exc()
                        result[res_type] = False
                else:
                    result[res_type] = False
        return result


    def create_app_res(self, files, name: str) -> None:
        self.generate_new_res(name)
        self.generate_res_files(files, name)


    def update_app_res(self, files, old: str, new: str) -> None:
        self.update_res(old, new)
        print("update_app_res")
        self.generate_res_files(files, new)


    def delete_res(self, name: str) -> None:
        if res.name_exist(self.res_path, name):
            res.delete(merge(self.res_path, name))


    def delete_tree_ress(self, name: str) -> None:
        pass
