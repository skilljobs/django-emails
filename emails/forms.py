from django import forms
from emails.models import MailoutCategory


def get_category_choices():
    qs = MailoutCategory.objects.filter(default=True)\
        .values_list('key', 'title')
    return list(qs)


class EmailPreferenceForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices=get_category_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
