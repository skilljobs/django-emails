from django.core.management.base import BaseCommand
from emails.imap_client import receive, IMAP4_SSL


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        receive(10 * 60)  # Cron will restart it every 10 mins.
        return ''  # empty string to avoid output
