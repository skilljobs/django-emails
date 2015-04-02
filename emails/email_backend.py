'''
Overrides the _send method of the default SMTP EmailBackend
class to include a DKIM signature based on settings:

DKIM_SELECTOR - e.g. 'selector' if using selector._domainkey.example.com
DKIM_DOMAIN - e.g. 'example.com'
DKIM_PRIVATE_KEY - full private key bytestring: e.g. b"""-----BEGIN RSA PRIVATE KEY-----..."""

Include in your settings file:
EMAIL_BACKEND = 'emails.email_backend.DKIMBackend'

Reguires dkim library; sudo pip3 install dkimpy
'''

from django.core.mail.backends.smtp import EmailBackend
import dkim
import settings

class DKIMBackend(EmailBackend):
    def _send(self, email_message):
        """A helper method that does the actual sending + DKIM signing."""
        if not email_message.recipients():
            return False
        try:
            message = email_message.message().as_bytes(linesep='\r\n')
            signature = dkim.sign(message,
                                  bytes(settings.DKIM_SELECTOR, 'utf8'),
                                  bytes(settings.DKIM_DOMAIN, 'utf8'),
                                  settings.DKIM_PRIVATE_KEY,
                                  include_headers=[b'from',])
            self.connection.sendmail(email_message.from_email,
                    email_message.recipients(),
                    signature+message)
        except:
            if not self.fail_silently:
                raise
            return False
        return True