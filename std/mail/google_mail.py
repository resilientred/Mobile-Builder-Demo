import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from builder.lib.model.entity.letter import Letter
from std.mail.mail import Mail


class GoogleMail(Mail):
    smtp_server: str = 'smtp.gmail.com'
    smtp_port: int = 465
    mail_lib = None


    def connect(self, login: str, password: str) -> None:
        self.mail_lib = smtplib.SMTP_SSL(host=self.smtp_server, port=self.smtp_port)
        self.mail_lib.login(login, password)


    def send_letter(self, letter: Letter) -> None:
        msg = MIMEMultipart()
        msg['From'] = letter.sender
        msg['To'] = letter.addressee
        msg['Subject'] = letter.title
        msg.attach(MIMEText(letter.message))

        if len(letter.files) > 0:
            for file in letter.files:
                with open(file, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=self.get_file_name(file)
                    )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % self.get_file_name(file)
                    msg.attach(part)

        print("Start sending mail " + letter.title)
        self.mail_lib.sendmail(letter.sender, letter.addressee, msg.as_string().encode('ascii'))
        print("Complete sending mail " + letter.title)


    @staticmethod
    def get_file_name(path: str) -> str:
        if path:
            elements = path.split("/")
            if elements:
                return elements[-1]
            else:
                pass
        else:
            pass
            # TODO ADD RAISE ERROR


    def disconnect(self) -> None:
        self.mail_lib.quit()
