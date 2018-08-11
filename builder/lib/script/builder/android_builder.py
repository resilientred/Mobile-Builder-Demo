import fileinput
import os
import re
import subprocess
from std.std import merge


def clone_android_repository():
    pass


# Set APK version for Google Play
def change_app_version(file_path, version_name, version_code):
    gradle_path = merge(file_path, '/app/build.gradle')

    with fileinput.FileInput(gradle_path, inplace=True) as file:
        code_regex = "versionCode\s(\d*)"  # Regex for parse versionCode
        name_regex = "versionName\s\"([^\"]+)\""  # Regex for parse versionName

        for line in file:
            # Find versionCode and change
            group_code = re.findall(code_regex, line, flags=re.MULTILINE)
            if len(group_code) > 0:
                line = line.replace(group_code[0], str(version_code))

            # Find versionName and change
            group_name = re.findall(name_regex, line, flags=re.MULTILINE)
            if len(group_name) > 0:
                line = line.replace(group_name[0], str(version_name))

            print(line, end='')


# Generate local.properties file with android SDK and NDK paths
def generate_local(final_path, sdk_path):
    sdk = "sdk.dir"
    local = "/local.properties"
    equal = "="

    file = open(merge(final_path, local), 'w+')
    file.writelines([sdk + equal + sdk_path, "\n"])
    file.close()


# Build final android project (Generate Release APK file)
def build_android_project(final_path, assets_path, release_params):
    path = "FINAL_PATH"
    store_file = "KEY_FILE"
    store_pass = "FILE_PASS"
    alias_key = "KEY_ALIAS"
    alias_pass = "ALIAS_PASS"

    script_path = merge(assets_path, '/build.sh')
    params = os.environ

    params[path] = final_path  # Put path to final project in variables environment
    params[store_file] = release_params[store_file]
    params[store_pass] = release_params[store_pass]
    params[alias_key] = release_params[alias_key]
    params[alias_pass] = release_params[alias_pass]

    # TODO REPLACE ON os.chmode
    subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
    subprocess.call([script_path], shell=True, env=params)  # Run script
