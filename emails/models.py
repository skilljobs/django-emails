from django.db import models
from django.conf import settings
from datetime import datetime


class Email(models.Model):
    """ Monitor emails sent """
    to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')
    subject = models.CharField(max_length=150)
    body = models.TextField()
    at = models.DateTimeField(default=datetime.now)
    bounced = models.BooleanField(default=False)

    prefetch = ['to']

    def __str__(self):
        return 'TO: %s, %s' % (self.to, self.subject)

    @models.permalink
    def get_absolute_url(self):
        return 'email', [self.pk]

    class Meta:
        db_table = 'emails'


class MailoutCategory(models.Model):
    key = models.CharField(max_length=12, primary_key=True)
    default = models.BooleanField()
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


class MailoutUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('emails.MailoutCategory')

    def __str__(self):
        return 'User #%s receives %s.' % (self.user_id, self.category_id)


def subscribe_all(user):
    for mc in MailoutCategory.objects.filter(default=True):
        mu = MailoutUser(user=user, category=mc)
        mu.save()


def unsubscribe_all(user):
    for mu in MailoutUser.objects.filter(user=user):
        mu.delete()
