from builder.lib.model.entity.letter import Letter


class LetterBuilder:

    @staticmethod
    def create_android_letter(type: str, version: str, sender: str, addressee: str, app_name: str, apk_path: str, message: str) -> Letter:
        sender = sender
        addressee = addressee
        title = f"{type} | {version} | {app_name.title()} | Gootax Mobile Builder"
        message = message
        files = [apk_path]
        return Letter(sender, addressee, title, message, files)


    @staticmethod
    def create_ios_cert_letter(sender: str, addressee: str, app_name: str, path_to_cert: str, message: str) -> Letter:
        sender = sender
        addressee = addressee
        title = f"Push Certificate | {app_name.title()} | Gootax Mobile Builder"
        message = message
        files = [path_to_cert]
        return Letter(sender, addressee, title, message, files)

