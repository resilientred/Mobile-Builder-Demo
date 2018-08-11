# -*- coding: utf-8 -*-
from std.mail.mail import GOOGLE_MAIL
from std.mail.mail import YANDEX_MAIL, Mail
from std.mail.yandex_mail import YandexMail

from std.mail.google_mail import GoogleMail


class MailFactory:

    @staticmethod
    def getMail(mail_type: str) -> Mail:
        if mail_type == YANDEX_MAIL:
            return YandexMail()
        if mail_type == GOOGLE_MAIL:
            return GoogleMail()

