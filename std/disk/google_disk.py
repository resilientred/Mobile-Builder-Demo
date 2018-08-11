from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from std import config
from std.disk.disk import Disk
from std.stdres import get_file_extension


class GoogleDisk(Disk):

    def __init__(self, with_auth: bool=False):
        self.drive: GoogleDrive = None
        if with_auth:
            self.auth()


    def auth(self) -> None:
        gauth = GoogleAuth(settings_file=config.DRIVE_SETTINGS_PATH)
        gauth.LoadCredentialsFile(config.DRIVE_CREDENTIALS_PATH)
        gauth.LoadClientConfigFile(config.DRIVE_SECRET_PATH)
        self.drive = GoogleDrive(gauth)


    def load_file(self, name: str, path: str, folder_id: str="root") -> bool:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file_item in file_list:
            if name == file_item['title']:
                file_id = file_item['id']
                file1 = self.drive.CreateFile({'id': file_id})
                file1.GetContentFile(path)
                return True
        return False


    def upload_file(self, path: str, name: str, folder_id: str=None) -> None:
        dot = "."

        if self.drive:
            file2 = self.drive.CreateFile()
            file2.SetContentFile(path)
            file2['title'] = name + dot + get_file_extension(path)
            if folder_id:
                file2['parents'] = [{"id": folder_id,
                                     "mimeType": "application/vnd.google-apps.folder"}]

            file2.Upload()
            print('Created file %s with mimeType %s' % (file2['title'],
                                                        file2['mimeType']))


    def check(self, name: str, folder_id: str="root") -> bool:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file in file_list:
            print(file)
            print(name)
            if file['title'] == name:
                return True
        return False


    def delete(self, name: str, folder_id: str="root") -> None:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file_item in file_list:
            if name == file_item['title']:
                file_id = file_item['id']
                temp_file = self.drive.CreateFile({'id': file_id})
                temp_file.Delete()


    def replace_file(self, path: str, name: str, folder_id: str="root") -> None:
        dot = "."
        print(name)

        title = name.split(dot)[0]
        self.delete(name, folder_id)
        self.upload_file(path, title, folder_id)


    def create_folder(self, name: str) -> None:
        folder_metadata = {'title': name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()


    def get_folder_id_by_name(self, name: str, folder_id: str="root") -> str:
        is_exist = self.check(name)
        if not is_exist:
            print("create folder")
            self.create_folder(name)
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file in file_list:
            if file['title'] == name:
                return file['id']


    def check_folder_id_by_name(self, name: str, folder_id: str="root") -> str:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
        for file in file_list:
            if file['title'] == name and file['mimeType'] == "application/vnd.google-apps.folder":
                return file['id']
