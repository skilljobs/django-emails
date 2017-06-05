from django.conf import settings


def fix_typo_email(user, new):
    pass


FIX_TYPO_EMAIL = getattr(settings, 'FIX_TYPO_EMAIL', fix_typo_email)
