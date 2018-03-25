from django import forms
from allauth.account.models import EmailAddress


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = ('email',)
