from django import forms
from django.contrib.auth.models import User
from .models import Hit


class FormManager(forms.Form):
    manager = forms.ModelChoiceField(queryset=(
        User.objects.filter(profile__type="boss").filter(profile__status='active')))
    user = forms.ModelChoiceField(queryset=User.objects.filter(
        profile__status="active"))


class FormStatus(forms.Form):
    change_status = forms.ChoiceField(choices=Hit.CHOICES)

    def __init__(self, actual_status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Hit.next_status(actual_status)
        self.fields["change_status"].choices = choices


class FormAssigned(forms.Form):
    assigned = forms.ModelChoiceField(
        label="Change assigned to",
        queryset=User.objects.filter(profile__status='active'))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.profile.is_boss:
            users = user.profile.manages.filter(profile__status='active')
        elif user.profile.is_leader:
            users = User.objects.filter(profile__status='active')
        else:
            users = User.objects.none()
        self.fields["assigned"].queryset = users
