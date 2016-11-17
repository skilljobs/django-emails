from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings
from emails.text_alt import render_as_text
from emails.models import MailoutUser, MailoutCategory
import logging

UNSUBSCRIBE_EMAIL = 'unsubscribe@' + settings.EMAIL_DOMAIN


def email(user, subj, template, context, check_pref=False,
          from_email=settings.DEFAULT_FROM_EMAIL):

    from emails.models import Email
    from subs.models import Subscription

    if user.bounce not in (None, 0, 1):  # 1 bounce is ok, but not more
        return False

    if check_pref:
        c = MailoutCategory.objects.get(pk=check_pref)
        s = MailoutUser.objects.filter(user=user, category=c).first()
        if not s:
            return

    subject = 'Hi %s, %s' % (user.first_name, subj)
    from_email = "%s <%s>" % (settings.NAME, from_email)
    if 'Feedback' in subj:
        subject = subj
    # subject must not contain newlines
    subject = ''.join(subject.splitlines())
    em = Email(to=user, subject=subject, body='')
    em.save()
    # add some generic_context
    context.update(settings.GENERIC_CONTEXT)
    context.update({
        'user': user,
        'subject': subj,  # use original short subject here
        'template': template,  # for tracking
        'em': em
    })

    body = render_to_string('emails/%s.html' % template, context)
    text = render_as_text(body)

    em.body = body + '<!--\n' + text + '\n-->'
    em.save()
    headers = {
        'List-Unsubscribe': '<mailto:%s>' % UNSUBSCRIBE_EMAIL,
        'X-EMAIL-ID': str(em.pk),
        'X-USER-ID': str(user.pk),
    }
    m = mail.EmailMultiAlternatives(subject, text, from_email,
                                    [user.email], headers=headers)
    m.attach_alternative(body, "text/html")
    # live or test, no sending in dev
    if not settings.DEBUG or hasattr(mail, 'outbox'):
        try:
            m.send()
        except Exception as e:
            logging.basicConfig(filename=settings.LOG)
            logging.warning(e)
            return False
    return True
