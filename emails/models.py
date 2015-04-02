from django.db import models
from datetime import datetime
import settings

class Email(models.Model):
    ''' Monitor emails sent '''
    to      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')
    subject = models.CharField(max_length=150)
    body    = models.TextField()
    at      = models.DateTimeField(default=datetime.now)
    
    prefetch = ['to']
    
    def __str__(self):
        return 'TO: %s, %s' % (self.to, self.subject)
    
    @models.permalink
    def get_absolute_url(self):
        if self.body:
            return 'email', [self.pk]
        return ''
    
    class Meta:
        db_table = 'emails'

class UserSubscription(models.Model):
    ''' Abstract subscription model to subclass.
    Add boolean fields to your subclass to make your own subscriptions
    named recieve_x; e.g.: receive_newsletter, receive_alerts etc.
    This will allow users to subscribe to different types of non-transactional emails.
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    receive_email = models.BooleanField('E-mail', default=True)
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        abstract = True