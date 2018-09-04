from django.urls import path
from emails.views import preferences
from emails.emails_views import emails
from emails.export import email_export

urlpatterns = [
    path('preferences', preferences,
         name='my_email_preferences'),
    path('preferences/<int:user_pk>', preferences,
         name='email_preferences'),
    path('emails/<int:pk>', emails, name='emails'),
    path('export', email_export, name='export'),
]
