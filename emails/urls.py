from django.urls import path
from emails.views import preferences, unsubscribe
from emails.emails_views import emails
from emails.export import email_export

urlpatterns = [
    path('preferences', preferences,
         name='my_email_preferences'),
    path('preferences/<int:user_pk>', preferences,
         name='email_preferences'),
    path('emails/<int:pk>', emails, name='emails'),
    path('unsubscribe/<int:user_pk>.<int:pk>.<slug:category>',
         unsubscribe,
         name='unsubscribe'),
    path('export', email_export, name='export'),
]
