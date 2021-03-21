from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class MailHandler:
    def __init__(self, name, email, verify_code):
        self.name = name
        self.email = email
        self.verify_code = verify_code

    def verify(self):
        email_template = render_to_string(
            'verify_mail.html',
            {'name': self.name, 'verify_code': self.verify_code}
        )

        email = EmailMessage(
            'Cometeor',
            email_template,
            settings.EMAIL_HOST_USER,
            [self.email]
        )

        email.fail_silently = False
        email.send()
