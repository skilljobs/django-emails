from django.conf import settings


def fix_typo_email(user, new):
    pass


EMAILS_FIX_TYPOS = getattr(settings, 'EMAILS_FIX_TYPOS', fix_typo_email)
