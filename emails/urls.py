from django.conf.urls import url
from emails.views import preferences
from emails.emails_views import emails
from emails.export import email_export

urlpatterns = [
    url(r'^preferences$', preferences, name='my_email_preferences'),
    url(r'^preferences/(?P<user_pk>[0-9]+)$', preferences, name='email_preferences'),
    url(r'^emails/(?P<pk>[0-9]+)$', emails, name='emails'),
    url(r'^export$', email_export, name='export'),
]
