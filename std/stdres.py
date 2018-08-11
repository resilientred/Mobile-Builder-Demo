import logging
import os
import shutil
import time
import zipfile

from backend.model.helper.app_helper import parse_sku
from std.error.data_error import DataError
from std.error.path_error import PathError
from std.error.res_error import ResourceError
from std.std import merge


# Unzip file to TEMP directory
def unzip_temp(file, zip_name: str, temp_res_path: str, res_type: str) -> None:
    filename = file.filename

    if not filename:
        raise DataEror(subcode=DataError.not_found,
                       data=DataError.not_found_mes % filename)

    if not allowed_zip(filename):
        raise ResourceError(subcode=ResourceError.file_type,
                            data=ResourceError.file_type_mes % (filename, "zip"))

    res_path = merge(temp_res_path, res_type)
    zip_path = merge(temp_res_path, zip_name)

    if os.path.exists(res_path):
        shutil.rmtree(res_path)
    os.makedirs(res_path)
    print(zip_path)
    file.save(zip_path)

    zip_ref = zipfile.ZipFile(zip_path, 'r')
    zip_ref.extractall(res_path)
    zip_ref.close()
    os.remove(zip_path)


def create_zip_res(archive_path, save_path):
    shutil.make_archive(base_name=save_path, format='zip', root_dir=archive_path)


# Move tree directory in new path
# NEED FOR MOVE FROM TEMP DIRECTORY
def save_temp(src: str, dst: str) -> None:
    if os.path.exists(dst):
        shutil.rmtree(dst)
    if not os.path.exists(src):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % src)
    shutil.copytree(src, dst)


# Validate and Save Json file
def save_json(file, path: str) -> None:
    filename = "google-services.json"

    if not allowed_json(filename):
        raise ResourceError(subcode=ResourceError.file_type,
                            data=ResourceError.file_type_mes % (file.filename, "json"))
    save_path = os.path.join(path, filename)
    os.makedirs(path)
    file.save(save_path)


# Rename existing res
def update(res_path: str, old: str, new: str) -> None:
    src = merge(res_path, old)
    dst = merge(res_path, new)

    if not os.path.exists(src):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % src)
    os.rename(src, dst)


# Create resource paths
def create(res_path: str, name: str) -> None:
    src = merge(res_path, name)

    if os.path.exists(src):
        raise PathError(subcode=PathError.path_exist,
                        data=PathError.path_exist_mes % src)

    os.makedirs(src)


# Validate path on existing and return bool result on delete path
def delete(path_to_res: str) -> None:
    if not os.path.exists(path_to_res):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % path_to_res)

    shutil.rmtree(path_to_res)


# Clearing path with final project on setted time
def clear_final_folders(finish_path: str, clear_time: int) -> None:
    begin_time_copy = time.time()
    list_of_dir = os.listdir(finish_path)
    count = 0

    for folder in list_of_dir:
        folder_path = finish_path + folder
        birthday = os.stat(folder_path).st_atime
        if birthday + clear_time > time.time():
            shutil.rmtree(folder_path)
            count += 1
    end_time_copy = time.time()

    logging.info("Total count REMOVE is " + str(count))
    logging.info("Total time REMOVE is " + str(end_time_copy - begin_time_copy))


# Validate resource name on existing
def name_exist(res_path: str, name: str) -> bool:
    return os.path.exists(merge(res_path, name))


def get_file_extension(path: str) -> str:
    path_bits: str = path.split("/")
    path_len: int = len(path_bits)
    if path_len:
        return path_bits[-1].split(".")[-1]


# Validate resource type on existing
def validate_type(path_to_res: str, res_type: str) -> bool:
    return os.path.exists(merge(path_to_res, res_type))


# Validate resource type on existing
def remote_validate_type(name: str, res_type: str, save_path: str, with_save: bool = False) -> bool:
    ANDROID = "android"
    IOS = "ios"
    GOOGLE = "google"
    from std.disk.google_disk import GoogleDisk

    drive = GoogleDisk(with_auth=True)

    if res_type == ANDROID or res_type == IOS:
        res_name = parse_sku(name) + "-" + res_type + ".zip"
    elif res_type == GOOGLE:
        res_name = "google-services.json"
    else:
        raise DataEror(subcode=DataError.not_found,
                       data=DataError.not_found_mes % name)

    print("remote_validate_type before %s" % res_name)
    is_exist = drive.check(res_name, drive.get_folder_id_by_name(name))
    print("remote_validate_type after %s" % is_exist)

    if not is_exist or not with_save:
        return is_exist
    elif is_exist and with_save:
        print("remote_validate_type is_exist")
        save_path = merge(save_path, res_type)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_file_path = merge(save_path, res_name)
        drive.load_file(res_name, save_file_path, drive.get_folder_id_by_name(name))
        if allowed_zip(res_name):
            print("remote_validate_type allowed_zip")
            print("remote_validate_type %s" % save_path)
            zip_ref = zipfile.ZipFile(save_file_path, 'r')
            zip_ref.extractall(save_path)
            zip_ref.close()
            os.remove(save_file_path)
        return True


# Validate ZIP file on name
def allowed_zip(filename: str) -> bool:
    if not filename:
        raise DataEror(subcode=DataError.not_found,
                       data=DataError.not_found_mes % filename)

    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "zip"


# Validate JSON file on name
def allowed_json(filename: str) -> bool:
    if not filename:
        raise DataEror(subcode=DataError.not_found,
                       data=DataError.not_found_mes % filename)

    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "json"


# Validate android images on existing and name
def validate_android_images(android_path: str) -> bool:
    if not os.path.exists(android_path):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % android_path)

    valid_dirs = ['logo', 'menulogo', 'push', 'splash']
    dpi = ["-mdpi", "-hdpi", "-xhdpi", "-xxhdpi"]
    png = ".png"

    dir_list = list(map(lambda x: str(x).lower(), os.listdir(android_path)))

    logging.info("Resource with path {%s} have {%s} folders" % (android_path, dir_list))

    for direct in valid_dirs:
        if direct not in dir_list:
            raise ResourceError(subcode=ResourceError.android_folder,
                                data=ResourceError.android_folder_mes % direct)

    for img_folder in dir_list:
        folder_path = merge(android_path, img_folder)

        if img_folder == "__MACOSX":
            continue
        if img_folder not in valid_dirs:
            try:
                shutil.rmtree(folder_path)
            except NotADirectoryError:
                os.remove(folder_path)
            continue

        images = list(map(lambda x: str(x).lower(), os.listdir(folder_path)))

        logging.info("Resource {%s} have {%s} images" % (img_folder, images))

        for image in images:
            if not image.startswith(img_folder):
                os.remove(merge(folder_path, image))

        for image_dpi in dpi:
            file = img_folder + image_dpi + png

            logging.info("Checking {%s} file" % file)

            if file not in images:
                raise ResourceError(subcode=ResourceError.android_image,
                                    data=ResourceError.android_image_mes % file)

    return True


# Validate android images on existing and name
def validate_ios_images(ios_path: str) -> bool:
    if not os.path.exists(ios_path):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % ios_path)

    valid_folders = ["appicon", "menulogo", "splash"]
    app_icon = 'appicon'
    menulogo = 'menulogo'
    splash = 'splash'

    scales_double = ["", "@2x"]
    scales_triple = ["", "@2x", "@3x"]
    scales_imagesets = ["@2x", "@3x"]

    images_triple = ["icon-60", "icon-small-40", "icon-small"]
    images_double = ["icon-76"]
    images_once = ["icon-167", "icon-20", "itunesartwork@2x"]

    splash_sizes = [
        "640x960",
        "640x1024",
        "640x1136",
        "750x1334",
        "768x1024",
        "1125x2436",
        "1242x2208",
        "1431x2000",
        "1536x2048",
        "2048x2732"
    ]

    png = ".png"
    dir_list = list(map(lambda x: str(x).lower(), os.listdir(ios_path)))

    logging.info("Resource with path {%s} have {%s} folders" % (ios_path, dir_list))

    for img_folder in dir_list:
        folder_path = merge(ios_path, img_folder)
        if img_folder == "__MACOSX":
            continue

        if img_folder not in valid_folders:
            try:
                shutil.rmtree(folder_path)
            except NotADirectoryError:
                os.remove(folder_path)
            continue

        images = list(map(lambda x: str(x).lower(), os.listdir(folder_path)))
        logging.info("Resource {%s} have {%s} images" % (img_folder, images))

        if img_folder == app_icon:
            for image in images_triple:
                for scale in scales_triple:
                    file = image + scale + png
                    if file not in images:
                        raise ResourceError(subcode=ResourceError.ios_image,
                                            data=ResourceError.ios_image_mes % img_folder + file)
            for image in images_double:
                for scale in scales_double:
                    file = image + scale + png
                    if file not in images:
                        raise ResourceError(subcode=ResourceError.ios_image,
                                            data=ResourceError.ios_image_mes % img_folder + file)
            for image in images_once:
                file = image + png
                if file not in images:
                    raise ResourceError(subcode=ResourceError.ios_image,
                                        data=ResourceError.ios_image_mes % img_folder + file)

        elif img_folder == menulogo:
            for scale in scales_imagesets:
                file = img_folder + scale + png
                logging.info("Checking {%s} file" % file)
                if file not in images:
                    raise ResourceError(subcode=ResourceError.ios_image,
                                        data=ResourceError.ios_image_mes % img_folder + file)
        elif img_folder == splash:
            for splash_size in splash_sizes:
                file = splash_size + png
                logging.info("Checking {%s} file" % file)
                if file not in images:
                    raise ResourceError(subcode=ResourceError.ios_image,
                                        data=ResourceError.ios_image_mes % img_folder + file)

    return True


# Validate android images on existing and name
def validate_ios_saved_images(ios_path: str) -> bool:
    if not os.path.exists(ios_path):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % ios_path)
    logo = "appicon"
    menulogo = "menulogo"
    logo_splash = "logo_splash"
    itunnes = "itunesartwork@2x"

    IDIOMS = ["iphone", "ipad"]

    idiom_iphone = "iphone"
    IPHONE_SCALES = ["@2", "@3"]
    IPHONE_SIZES = ["20x20", "29x29", "40x40", "60x60"]

    idiom_ipad = "ipad"
    IPAD_SIZES = ["20x20", "29x29", "40x40", "76x76", "83.5x83.5"]
    IPAD_SCALES = ["@1", "@2"]
    scales_imagesets = ["@2", "@3"]

    splash_sizes = [
        "640x960",
        "640x1024",
        "640x1136",
        "750x1334",
        "1024x768",
        "1125x2436",
        "1242x2208",
        "1431x2000",
        "2048x1536",
        "2048x2732"
    ]

    png = ".png"
    dir_list = os.listdir(ios_path)

    logging.info("Resource with path {%s} have {%s} folders" % (ios_path, dir_list))

    for img_folder in dir_list:
        folder_path = merge(ios_path, img_folder)
        if img_folder == "__MACOSX":
            continue
        try:
            images = os.listdir(folder_path)
        except Exception:
            return False
        logging.info("Resource {%s} have {%s} images" % (img_folder, images))

        if img_folder == logo:
            for idiom in IDIOMS:
                if idiom == idiom_iphone:
                    for size in IPHONE_SIZES:
                        for scale in IPHONE_SCALES:
                            image = logo + "-" + idiom_iphone + size + scale + png
                            if image not in images:
                                print(f"Not image {image}")
                                return False
                if idiom == idiom_ipad:
                    for size in IPAD_SIZES:
                        for scale in IPAD_SCALES:
                            image = logo + "-" + idiom_ipad + size + scale + png
                            if image not in images:
                                print(f"Not image {image}")
                                return False

        elif img_folder == menulogo:
            for scale in scales_imagesets:
                file = img_folder + scale + png
                logging.info("Checking {%s} file" % file)
                if file not in images:
                    return False
        elif img_folder == logo_splash:
            for splash_size in splash_sizes:
                file = splash_size + png
                logging.info("Checking {%s} file" % file)
                if file not in images:
                    return False
    return True


# Validate Google Play JSON on existing
def validate_google_push(google_path: str) -> bool:
    if not os.path.exists(google_path):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % google_path)

    google_service = "google-services.json"
    paths = os.listdir(google_path)
    logging.info("Google path {%s} have {%s} file" % (google_path, paths))

    for path in paths:
        if path != google_service:
            raise ResourceError(subcode=ResourceError.google_res,
                                data=ResourceError.google_res_mes % path)

    return True


# Validate android images on existing and name
def validate_driver_images(android_path: str) -> bool:
    if not os.path.exists(android_path):
        raise PathError(subcode=PathError.path_not_found,
                        data=PathError.path_not_found_mes % android_path)

    valid_dirs = ['ic_launcher', 'gootax', 'push', 'splash']
    dpi = ["-mdpi", "-hdpi", "-xhdpi", "-xxhdpi"]
    png = ".png"

    dir_list = list(map(lambda x: str(x).lower(), os.listdir(android_path)))

    logging.info("Resource with path {%s} have {%s} folders" % (android_path, dir_list))

    for direct in valid_dirs:
        if direct not in dir_list:
            raise ResourceError(subcode=ResourceError.android_folder,
                                data=ResourceError.android_folder_mes % direct)

    for img_folder in dir_list:
        folder_path = merge(android_path, img_folder)

        if img_folder == "__MACOSX":
            continue
        if img_folder not in valid_dirs:
            try:
                shutil.rmtree(folder_path)
            except NotADirectoryError:
                os.remove(folder_path)
            continue

        images = list(map(lambda x: str(x).lower(), os.listdir(folder_path)))

        logging.info("Resource {%s} have {%s} images" % (img_folder, images))

        for image in images:
            if not image.startswith(img_folder):
                os.remove(merge(folder_path, image))

        for image_dpi in dpi:
            file = img_folder + image_dpi + png

            logging.info("Checking {%s} file" % file)

            if file not in images:
                raise ResourceError(subcode=ResourceError.android_image,
                                    data=ResourceError.android_image_mes % file)

    return True

