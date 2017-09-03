from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory as inline
from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.models import EmailAddress
from emails.emails_forms import EmailForm
from emails.confirm import send_confirm_primary

User = get_user_model()


@login_required
def emails(request, pk):
    """A way for staff to manage email addresses of users
    """
    if not request.user.is_staff:
        return HttpResponse('')

    user = User.objects.get(pk=pk)

    data = []
    if request.method == 'POST':
        data = (request.POST,)

    formset = inline(User, EmailAddress, EmailForm, BaseInlineFormSet,
                     extra=0, can_delete=False, max_num=6)
    emails = formset(*data, instance=user)

    if emails.is_valid():
        for e in emails.forms:
            f = e.save()

    em = EmailAddress.objects.filter(user=user, primary=True).first()
    user.email = em.email
    user.save()
    send_confirm_primary(user)

    return render(request, 'emails/emails.html', {
        'user': user,
        'emails': emails
    })
