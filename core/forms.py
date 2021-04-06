from django import forms
from django.contrib.auth.models import User
from .models import Hit


class FormManager(forms.Form):
    manager = forms.ModelChoiceField(queryset=User.objects.filter(profile__type="boss"))
    user = forms.ModelChoiceField(queryset=User.objects.all())

class FormStatus(forms.Form):
    change_status = forms.ChoiceField(choices=Hit.CHOICES)

    def __init__(self, actual_status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Hit.next_status(actual_status)
        self.fields["change_status"].choices = choices


class FormAssigned(forms.Form):
    assigned = forms.ModelChoiceField(label="Change assigned to",
                                      queryset=User.objects.all())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.profile.is_boss:
            users = user.profile.manages.all()
        elif user.profile.is_leader:
            users = User.objects.all()
        else:
            users = User.objects.none()
        self.fields["assigned"].queryset = users
