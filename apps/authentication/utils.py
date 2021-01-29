from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data.get("subject"), body=data.get("body"), to=[data.get("to")]
        )
        email.send()