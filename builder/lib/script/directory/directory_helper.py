import errno
import logging
import os
import shutil
import time

from std.log import log_info as info
from std.std import merge


class DirectoryHelper:

    def __init__(self, final_path, root_path):
        self.final_path = final_path
        self.root_path = root_path

    # RENAME PROJECT PATHS
    def copy_sample_project(self):
        begin_time_copy = time.time()

        try:
            shutil.copytree(self.root_path, self.final_path)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy2(self.root_path, self.final_path)
            else:
                raise
        end_time_copy = time.time()
        logging.info("Total time COPY is " + str(end_time_copy - begin_time_copy))


    def replace_strings(self, bundle, new_bundle):
        print(f"old {bundle}")
        print(f"new {new_bundle}")
        # Begin function
        begin_time = time.time()
        project_path = self.final_path
        count_total = 0
        total_replace = 0
        count_error = 0

        for path, dirs, files in os.walk(project_path, True):
            for cur_name in files:
                count_total += 1
                file_path = merge(path, cur_name)
                try:
                    text = open(file_path).read()
                    if bundle in text:
                        open(file_path, 'w').write(text.replace(bundle, new_bundle))
                        total_replace += 1

                except ValueError:
                    count_error += 1
        # End function work

        end_time = time.time()
        executing_time = end_time - begin_time
        logging.info(info.FILE_REPLACE % (str(count_total), str(total_replace), str(count_error), str(executing_time)))


    def replace_app_dirs(self, app_name_id, bundle):
        # Begin function work
        begin_time = time.time()
        project_path = self.final_path
        count_total = 0
        total_replace = 0
        count_error = 0

        for path, dirs, files in os.walk(project_path, True):
            for cur_dir in dirs:
                count_total += 1
                if cur_dir == "client":
                    try:
                        total_replace += 1
                        path_to_replace = merge(path, cur_dir)
                        path_in_replace = merge(path, app_name_id)
                        path = str(bundle).replace(".", "/")
                        new_path = merge(self.final_path + "/app/src/main/java/", path)
                        if new_path == path_to_replace:
                            continue
                        os.rename(path_to_replace, path_in_replace)
                        logging.info(info.DIR_RENAME_SUCCESS % path_to_replace)
                    except FileNotFoundError:
                        count_error += 1
                        logging.error("Exception rename " + cur_dir)
        # End function work

        end_time = time.time()
        executing_time = end_time - begin_time
        logging.info(info.DIRS_REPLACE % (str(count_total), str(total_replace), str(count_error), str(executing_time)))

    def replace_app_driver_dirs(self, app_name_id, bundle):
        # Begin function work
        begin_time = time.time()
        project_path = self.final_path
        count_total = 0
        total_replace = 0
        count_error = 0

        for path, dirs, files in os.walk(project_path, True):
            for cur_dir in dirs:
                count_total += 1
                if cur_dir == "driver":
                    try:
                        total_replace += 1
                        path_to_replace = merge(path, cur_dir)
                        path_in_replace = merge(path, app_name_id)
                        path = str(bundle).replace(".", "/")
                        new_path = merge(self.final_path + "/app/src/main/java/", path)
                        if new_path == path_to_replace:
                            continue
                        os.rename(path_to_replace, path_in_replace)
                        logging.info(info.DIR_RENAME_SUCCESS % path_to_replace)
                    except FileNotFoundError:
                        count_error += 1
                        logging.error("Exception rename " + cur_dir)
        # End function work

        end_time = time.time()
        executing_time = end_time - begin_time
        logging.info(info.DIRS_REPLACE % (str(count_total), str(total_replace), str(count_error), str(executing_time)))

    def replace_android_bundle(self, bundle):
        def_path = merge(self.final_path, 'app/src/main/java/com/gootax/client')
        path = str(bundle).replace(".", "/")
        new_path = merge(self.final_path + "/app/src/main/java/", path)
        os.renames(def_path, new_path)

    def replace_android_driver_bundle(self, bundle):
        def_path = merge(self.final_path, 'app/src/main/java/com/gootax/driver')
        path = str(bundle).replace(".", "/")
        new_path = merge(self.final_path + "/app/src/main/java/", path)
        os.renames(def_path, new_path)

    def replace_ios_bundle(self, bundle, new_bundle):
        # Begin function work
        begin_time_replace = time.time()
        count_total = 0
        count_file_replace = 0
        count_error = 0

        for path, dirs, files in os.walk(self.final_path, True):
            for cur_name in files:
                count_total += 1
                file_path = merge(path, cur_name)
                try:
                    text = open(file_path).read()
                    if bundle in text:
                        open(file_path, 'w').write(text.replace(bundle, new_bundle))
                        count_file_replace += 1

                except ValueError:
                    count_error += 1
        # End function work
        end_time_replace = time.time()
        print("_________________________________________")
        print("Total inspect file count is " + str(count_total))
        print("Total FILE replace count is " + str(count_file_replace))
        print("Error count is " + str(count_error))
        print("Total time REPLACE is " + str(end_time_replace - begin_time_replace))


    # RENAME PROJECT PATHS
    def remove_final_project(self):
        begin_time_copy = time.time()
        if os.path.exists(self.final_path):
            shutil.rmtree(self.final_path)
        end_time_copy = time.time()
        logging.info(info.DIR_REMOVE % (str(end_time_copy - begin_time_copy)))
