from django.views import generic
from django.urls import reverse_lazy
from django.http import Http404
from ..forms import FormManager
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class ManageHitman(generic.FormView):
    form_class = FormManager
    template_name = "core/manage_users.html"
    success_url = reverse_lazy("manage")

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        if self.request.user.profile.is_leader:
            form.fields["manager"].queryset = User.objects.filter(profile__type="boss")
        else:
            form.fields["manager"].queryset = User.objects.filter(id=self.request.user.id)
        return form

    def form_valid(self, form):
        if self.request.user.profile.is_leader:
            user = form.cleaned_data.get("manager")
            return self._form_valid(form, user)
        elif self.request.user.profile.is_boss:
            user = self.request.user
            return self._form_valid(form, user)
        else:
            raise Http404("not allowed")

    def _form_valid(self, form, user):
        newuser = form.cleaned_data.get("user")
        if not user.profile.manages.filter(id=newuser.id).exists():
            user.profile.manages.add(newuser)
            messages.success(self.request, "Hitman was added to my charge")
        else:
            user.profile.manages.remove(newuser)
            messages.info(self.request, "Hitman was removed to my charge")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        from ..models import Profile
        context = super().get_context_data(**kwargs)
        if self.request.user.profile.is_leader:
            context.update({
                'bosses': Profile.objects.filter(type="boss")
            })
        else:
            context.update({
                'bosses': [self.request.user.profile]
            })

        return context


manages = login_required(ManageHitman.as_view())
