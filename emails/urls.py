from django.conf.urls import url
from emails.views import preferences

urlpatterns = [
    url(r'^preferences$', preferences, name='my_email_preferences'),
    url(r'^preferences/(?P<user_pk>[0-9]+)$', preferences, name='email_preferences'),
]
