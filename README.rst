Emails: python mailing and processing for high volume senders and recipients
============================================================================

There's more to successful email campaings than just sending pretty html email.
What's important is that it gets delivered and read.

...and when email gets delivered, sender will receive a lot of emails too, automated and hand-typed, and will need to process it.

This app contains a set of tools needed including:

Simple IMAP client for instant prosessing of received email (recipes):

- bounces
- unsubscribes via feedback loop replies for major email providers (Yahoo, AOL, Outlook-Hotmail...)
- unsubscribes via replies to unsubscribe headers (Gmail and others)
- processing of attachements for upload (via separate upload app)

- convert HTML email to TEXT alternative
- DKIM (DomainKeys Identified Mail) and DNS measures
- email storage and archiving
- responsive HTML emails


DNS measures
------------
These increase delivery rate and protect from email spoofing ensuring your email is more likely to reach inbox rather than spam folder.

**SPF record*** (Sender policy framework) needs adding to DNS records
of the sender to specify which servers are allowed to send email from given domain.

This can be a simple DNS record:

	@    TXT/SPF    v=spf1 a mx ~all

**PTR or Pointer record** used to check if the domain name is matching
with the IP address from where the connection was initiated.
Set it up for a VM sending email using reverse DNS. `https://www.linode.com/docs/networking/dns/setting-reverse-dns Linode guide`_

**DKIM records** are DNS records containing public domain key used for checking agains signature on each email produced by private key:

    [DKIM_SELECTOR]._domainkey    TXT/SPF    k=rsa; p=[DKIM public key]
	_domainkey                    TXT/SPF    o=~; r=[DEFAULT_FROM_EMAIL]

Features included so far:

- DKIM backend to sign emails using domain keys
- IMAP client processing recipes for incoming email
- Text alternatives