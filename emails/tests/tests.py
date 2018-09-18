"""Test IMAP bounce alert and upload.
"""
from django.test import TestCase
from django.core.mail import EmailMessage
from django.conf import settings
from emails import imap_client
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os.path

EMAIL = settings.DEFAULT_FROM_EMAIL
UPLOAD_FILE = settings.STATIC_ROOT + '/i/help.jpg'
UPLOAD_EMAIL = 'upload@' + settings.EMAIL_DOMAIN
SIGNUP_EMAIL = 'test@' + settings.EMAIL_DOMAIN
SSL = {'wsgi.url_scheme': 'https', 'HTTP_X_FORWARDED_SSL': 'TLSv1'}


def send_email(subject='', to=EMAIL, sender=EMAIL, photo=0):
    """Send emails on dev during tests with standard test runner
    """
    m = MIMEMultipart()
    m['Subject'] = subject
    m['To'] = to
    m['From'] = sender
    if photo:
        img = MIMEImage(open(photo, 'rb').read())
        img.add_header('Content-Disposition', 'attachment',
                       filename=os.path.basename(photo))
        m.attach(img)
    part = MIMEText('text', "plain")
    part.set_payload(SIGNUP_EMAIL)
    m.attach(part)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(EMAIL, settings.EMAIL_PASSWORD)
    s.sendmail(sender, to, m.as_string())
    s.quit()


def test_email_upload():
    # email JPEG attachement
    send_email('Upload test', to=UPLOAD_EMAIL,
               sender=SIGNUP_EMAIL,
               photo=UPLOAD_FILE)
    imap_client.receive(5)


class ImapTestCase(TestCase):
    def test_imap(self):
        send_email('undeliverable')
        test_email_upload()
