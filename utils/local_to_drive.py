import os
import shutil

from backend.model.helper.app_helper import parse_sku
from std import stdres as res
from std.config import RES_PATH, STATIC_PATH
from std.disk.google_disk import GoogleDisk
from std.std import merge


def load_files_to_drive(path):
    platforms = ["android", "ios"]
    disk = GoogleDisk(with_auth=True)
    list_dirs = os.listdir(path)

    json_name = "google-services.json"

    for proj_dir in list_dirs:
        print(proj_dir)
        project_path = merge(RES_PATH, proj_dir)

        try:
            json_path = merge(project_path, "google", json_name)
            disk.replace_file(json_path, json_name, disk.get_folder_id_by_name(proj_dir))
        except Exception as e:
            print(e)

        for platform in platforms:
            try:
                platform_path = merge(project_path, platform)
                res.create_zip_res(platform_path, merge(project_path, parse_sku(proj_dir) + "-" + platform))
                print(platform_path)

                gzip_name = parse_sku(proj_dir) + "-" + platform + ".zip"
                gzip_path = merge(project_path, gzip_name)
                print(gzip_path)
                disk.replace_file(gzip_path, gzip_name, disk.get_folder_id_by_name(proj_dir))

                os.remove(gzip_path)
                print("success")
            except Exception as e:
                print("error")


def update_images(path, static_path):
    platforms = ["android", "ios"]
    disk = GoogleDisk(with_auth=True)
    list_dirs = os.listdir(path)


    for proj_dir in list_dirs:
        print(proj_dir)
        project_path = merge(RES_PATH, proj_dir)

        image_path = merge(project_path, "android", "logo", "logo-xxhdpi.png")
        if os.path.exists(image_path):
            print("copy start")
            dest_path = merge(static_path, "icon", proj_dir.replace(".", "_") + ".png")
            shutil.copy(image_path, dest_path)
            print("copy end")


update_images(RES_PATH, STATIC_PATH)
# load_files_to_drive(RES_PATH)

# disk = GoogleDisk(with_auth=True)
# print(disk.get_folder_id_by_name("com.gootax.k666"))
# shutil.rmtree(merge(RES_PATH, "com.gootax.fsd"))
