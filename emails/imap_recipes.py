from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from emails import send
from emails.models import Email, unsubscribe_all
import re

User = get_user_model()

EMAIL_RE = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')


def get_user(email):
    """ Sometimes user account is setup using @gmail.com domain,
    but android phone says @googlemail.com and vice versa
    """
    try:
        if 'googlemail' in email or 'gmail' in email:
            uname = email.partition('@')[0]
            users = User.objects.filter(Q(email=uname+'@googlemail.com') |
                                        Q(email=uname+'@gmail.com'))
        else:
            users = User.objects.filter(email=email)
        u = users.order_by('-seen')[0]
        return u
    except (IndexError, User.DoesNotExist):
        if settings.DEBUG:
            print('no such address: ' + email)  # don't notify the sender
        return False


def unsubscribe_email(email):
    user = get_user(email)
    if not user:
        return f'No such user {email}'
    for ad in user.ad_set.all():
        ad.off = True
        ad.save(staff=True)
    unsubscribe_all(user)
    return f'Turned off ads for {email}.'


def unsubscribe(msg):
    """ Process automated spam reports/unsubscribes
    from different email providers.
    """
    try:
        sender = msg['From']
    except IndexError:
        return 'No sender.'
    # Yahoo & Hotmail
    if 'feedback@arf.mail.yahoo.com' in sender or\
       'staff@hotmail.com' in sender:
        if msg.is_multipart():
            for part in msg.walk():
                to = part['To']
                if to:
                    if settings.EMAIL_DOMAIN in to:
                        continue
                    return unsubscribe_email(to)
    # Unsubscribe header (GMail etc.)
    if msg['To'] == 'unsubscribe@'+settings.EMAIL_DOMAIN:
        for user_email in EMAIL_RE.findall(sender):
            return unsubscribe_email(user_email)
    # AOL feedback loop is redacted, so we pull user ID from message
    if sender == 'scomp@aol.net':
        try:
            user_id = str(msg).split('/user/')[1].split('?')[0]
            user = User.objects.get(pk=user_id)
            return unsubscribe_email(user.email)
        except Exception as e:
            return 'AOL unsubscribe failed:', e, str(msg)


def note_bounce(msg):
    """
    Process bounced mail
    --------------------
    Count bounces and save this for every user.
    Elsewhere:
        Alert user that likely mistyped email address and prompt to change.
        Reset bounce count if email address changed.
        Do not email the address again if there was more than 1 bounce.

    Gmail filter:
        subject:("delivery status notification"|"returned mail: user unknown"/
                  |"undeliverable"|"mail delivery failed"|"failure notice"/
                  |"delivery failure"|"returned to sender"/
                  |"there was an error sending your mail")
        ...Apply label "Process/Bounces", Never send it to Spam
    """
    addresses = list(set(EMAIL_RE.findall(str(msg))))
    addresses = [x for x in addresses
                 if settings.EMAIL_DOMAIN not in x and
                 'mailer-daemon@' not in x.lower() and
                 'postmaster@' not in x.lower() and
                 'mx.google.com' not in x.lower()]
    for address in addresses:
        if settings.DEBUG:
            print(address)
        user = get_user(address)
        if user:
            email = Email.objects.filter(to=user).last()
            email.bounced = True
            email.save()
            if hasattr(user, 'profile'):
                if not user.profile.bounce:
                    user.profile.bounce = 0
                user.profile.bounce += 1
                user.profile.save()
            if settings.DEBUG:
                print("Bounce noted.")
    if settings.DEBUG:
        return 'Done.'
