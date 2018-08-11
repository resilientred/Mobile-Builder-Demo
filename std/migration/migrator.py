import os

from std.std import merge


''' --------------------------------------------------- DEPRECATED ------------------------------------------------- '''
'''
RES_LIST_PATH = "PATH"
res_man = ResourceManager(config.RES_PATH, config.TEMP_PATH)


def migrate_google_res() -> None:
    dir_list: list = os.listdir(RES_LIST_PATH)
    for folder in dir_list:
        res_path = merge(RES_LIST_PATH, folder)
        json_list = list(map(lambda x: validate_files(x), os.listdir(res_path)))
        map(lambda json: res_man.generate_google_res(merge(res_path, json), folder), json_list)


def migrate_android_res() -> None:
    dir_list: list = os.listdir(RES_LIST_PATH)
    for folder in dir_list:
        res_path = merge(RES_LIST_PATH, folder)
        json_list = list(map(lambda x: validate_files(x), os.listdir(res_path)))
        map(lambda json: res_man.generate_google_res(merge(res_path, json), folder), json_list)


# Std res extensions
def validate_files(path: str) -> str:
    if res.allowed_json(path):
        return path

'''


def rename_paths():
    import os
    res_path = "/Users/andrew/PycharmProjects/python-build-script-res/resource/res"
    dirs = os.listdir(res_path)
    print(dirs)
    for x in dirs:
        rename(path=res_path, x=x)


def rename(path, x):
    print(merge(path, x))
    os.rename(merge(path, x), merge(path, "com.gootax." + x))

