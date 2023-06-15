from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Email(models.Model):
    """Monitor emails sent."""
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails',
                           on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    body = models.TextField()
    at = models.DateTimeField(default=timezone.now)
    bounced = models.BooleanField(default=False)

    prefetch = ['to', 'to__subscription']

    def __str__(self):
        return f'TO: {self.to}, {self.subject}'

    def get_absolute_url(self):
        return reverse('email', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'emails'


class MailoutCategory(models.Model):
    """Category of emails being sent out."""
    key = models.CharField(max_length=12, primary_key=True)
    default = models.BooleanField()  # default subscribed
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.key


class MailoutUser(models.Model):
    """Consent to send a category of emails to a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    category = models.ForeignKey('emails.MailoutCategory',
                                 on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'User #{self.user_id} receives {self.category_id}.'


def subscribe_user_to(user, category_key):
    mc = MailoutCategory.objects.filter(key=category_key).first()
    if mc:
        mu = MailoutUser(user=user, category=mc)
        mu.save()
        return mu
    return


def subscribe_all(user):
    for mc in MailoutCategory.objects.filter(default=True):
        mu = MailoutUser(user=user, category=mc)
        mu.save()


def unsubscribe_all(user):
    for mu in MailoutUser.objects.filter(user=user):
        mu.delete()
