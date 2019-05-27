from django.core.management.base import BaseCommand
from emails.imap_client import receive, IMAP4_SSL


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            receive(10 * 60)  # Cron will restart it every 10 mins.
        except IMAP4_SSL.abort:
            return ''  # no output
