from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings
from emails.text_alt import render_as_text
import logging

UNSUBSCRIBE_EMAIL = 'unsubscribe@' + settings.EMAIL_DOMAIN


def email(user, subj, template, context, check_pref=False,
          from_email=settings.DEFAULT_FROM_EMAIL):

    from emails.models import Email
    from subs.models import Subscription

    if check_pref:
        s, created = Subscription.objects.get_or_create(user=user)
        ok = getattr(s, 'receive_' + check_pref)
        if not ok:
            return

    subject = 'Hi %s, %s' % (user.first_name, subj)
    from_email = "%s <%s>" % (settings.NAME, from_email)
    if 'Feedback' in subj:
        subject = subj
    # subject must not contain newlines
    subject = ''.join(subject.splitlines())
    # add some generic_context
    context.update(settings.GENERIC_CONTEXT)
    context.update({
        'user': user,
        'subject': subj,  # use original short subject here
        'template': template  # for tracking
    })
    body = render_to_string('emails/%s.html' % template, context)
    text = render_as_text(body)
    try:
        if user.bounce in (None, 0, 1):  # 1 bounce is ok, but not more
            em = Email(to=user, subject=subject,
                       body=body + '<!--\n%s\n-->' % text)
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
                m.send()
            return True
    except Exception as e:
        logging.basicConfig(filename=settings.LOG)
        logging.warning(e)
    return False
