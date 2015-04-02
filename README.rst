Emails: python mailing and processing for high volume senders and recipients
============================================================================

There's more to successful email campaings than just sending pretty html email.
What's important is that it gets delivered and read.

...and when email gets delivered, sender will receive a lot of emails too, automated and hand-typed, and will need to process it.

Measures that need to be in place include:

- bounce processing
- feedback loop processing for major email providers (Yahoo, AOL, Outlook-Hotmail...)
- unsubscribe headers (Gmail and others)
- unsubscribes processing
- email storage and archiving
- responsive HTML emails
- Text alternatives
- DKIM (DomainKeys Identified Mail) and DNS measures
	- SPF record (Sender policy framework) needs adding to DNS records
	of th asender to specify which servers are allowed to send email from given domain.
	- PTR (Pointer record) used to check if the server name is actually
	associated with the IP address from where the connection was initiated.

Features:
- DKIM backend
- Text alternatives