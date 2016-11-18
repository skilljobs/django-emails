from django import forms
from emails.models import MailoutCategory


class EmailPreferenceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=list(MailoutCategory.objects.filter(default=True)\
                                            .values_list('key', 'title')),
        widget=forms.CheckboxSelectMultiple
    )
