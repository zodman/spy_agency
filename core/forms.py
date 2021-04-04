from django import forms
from django.contrib.auth.models import User
from .models import Hit


class FormStatus(forms.Form):
    change_status = forms.ChoiceField(choices=Hit.CHOICES)

    def __init__(self, actual_status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Hit.next_status(actual_status)
        self.fields["change_status"].choices = choices


class FormAssigned(forms.Form):
    assigned = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = user.profile.manages.all()
        self.fields["assigned"].queryset = users
