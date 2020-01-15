"""Django allauth bulk email confirmation utility.
"""
from django.test import RequestFactory
from django.conf import settings
from allauth.account.models import EmailAddress


def reset_bounces(profile):
    profile.bounce = None
    profile.save()


def send_confirm_primary(user, request=False):
    """Confirm primary email address when request is not available.
    https://github.com/pennersr/django-allauth/issues/933
    """
    reset_bounces(user)
    if not request:
        request = RequestFactory().get('/', SERVER_NAME=settings.DOMAIN)
    email, created = EmailAddress.objects.get_or_create(
                                 user=user, email=user.email)
    if not email.primary:
        email.set_as_primary()
    email.send_confirmation(request)
