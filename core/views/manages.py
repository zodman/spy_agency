from django.views import generic
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.html import format_html
from ..forms import FormManager
from ..models import Profile
from django_tables2 import SingleTableView
from django_tables2.utils import A
import django_tables2 as table
from django import forms


class MixinRestrictedHitman:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.profile.is_hitman:
            raise Http404("not allowed")
        elif user.profile.is_boss:
            qs = qs.filter(manages=user)
        return qs


class HitmanUpdateView(MixinRestrictedHitman, generic.UpdateView):
    model = Profile

    def get_form_class(self):
        if self.request.user.profile.is_leader:
            return forms.modelform_factory(Profile,
                                           fields=('status', "description", "type",))
        return forms.modelform_factory(Profile,
                                       fields=('status', "description",))

    def form_valid(self, form):
        messages.success(self.request, "Updated Hitman")
        return super().form_valid(form)

class HitmanDetail(MixinRestrictedHitman, generic.DetailView):
    model = Profile
    template_name = "core/profile_detail.html"

class ProfileTable(table.Table):
    actions = table.LinkColumn("hitman_detail", kwargs={'pk': A('pk')},
                               text="Detail")
    status = table.Column()

    def render_status(self, value, record):
        return format_html(
            f"<span class='tag is-{record.status_color} is-light'>{value}</span>"
        )

    class Meta:
        model = Profile
        fields = ("user__username", 'type', "status")

class HitmenView(MixinRestrictedHitman, SingleTableView):
    model = Profile
    table_class = ProfileTable
    template_name = "core/profile_list.html"


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
hitmen = login_required(HitmenView.as_view())
hitman_detail = login_required(HitmanDetail.as_view())
hitman_update = login_required(HitmanUpdateView.as_view())


__all__ = [
    'hitmen',
    'manages',
    'hitman_detail',
    'hitman_update',
]
