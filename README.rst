Emails: python mailing and processing for high volume senders and recipients
============================================================================

There's more to successful email campaigns than just sending pretty html email.
Important is that email gets delivered and read ...and when it does, sender
will receive a lot of emails too, automated and hand-typed, and will need
to process them.

This app contains a set of tools needed including:

- Simple IMAP client for instant processing of received email (recipes):

	- bounces
	- un-subscribes via feedback loop replies for major email providers
	(Yahoo, AOL, Outlook/Hotmail...)
	- un-subscribes via replies to unsubscribe headers (GMail and others)
	- processing of attachments for upload (via separate upload app)

- convert HTML email to TEXT alternative
- DKIM (DomainKeys Identified Mail) and DNS measures
- email storage and archiving
- managing user's subscriptions to email categories
- responsive HTML email template

Read: `GMail Bulk Senders Guidelines <https://support.google.com/mail/answer/81126>`_

DNS measures
------------
These increase delivery rate and protect from email spoofing ensuring
your email is more likely to reach inbox rather than spam folder.

SPF records
~~~~~~~~~~~
Sender policy framework records needs adding to DNS records
of the sender to specify which servers are allowed to send email
from given domain.

This can be a simple DNS record::

	@    TXT/SPF    v=spf1 a mx ~all

PTR or Pointer record
~~~~~~~~~~~~~~~~~~~~~
Pointer record is used to check if the domain name is matching
with the IP address from where the connection was initiated.
Set it up with your hosting company for a VM sending your emails using
`reverse DNS (Linode guide) <https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/>`_

DKIM records
~~~~~~~~~~~~
These DNS records contain public domain key used for checking against
signature on each email produced by private key::

    [DKIM_SELECTOR]._domainkey    TXT/SPF    k=rsa; p=[DKIM public key]
	_domainkey                TXT/SPF    o=~; r=[DEFAULT_FROM_EMAIL]
