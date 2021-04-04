from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from core.models import Hit
from django.db.models import Q
import django_tables2 as table
import django_filters
import django_filters.views
from .forms import FormStatus, FormAssigned

class HitFilter(django_filters.FilterSet):
    target = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Hit
        fields = ("target", "created_by", "status")


class HitTable(table.Table):
    actions = table.TemplateColumn(template_name="_column_actions.html")
    status = table.Column()

    def render_status(self, value, record):
        return format_html(f"<span class='tag is-{record.status_color} is-light'>{value}</span>")

    class Meta:
        model = Hit
        exclude = ("description", "created_at", "updated_at")


class MixinRestricted:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.profile.is_hitman:
            qs = qs.filter(assigned=user)
        elif user.profile.is_boss:
            qs = qs.filter(Q(created_by=user)|Q(assigned=user))
        return qs


class Dashboard(MixinRestricted, table.SingleTableMixin, django_filters.views.FilterView):
    template_name = "dashboard.html"
    model = Hit
    table_class = HitTable
    filterset_class = HitFilter


class HitView(MixinRestricted, generic.DetailView):
    model = Hit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        user = self.request.user
        if Hit.next_status(object.status) and user.profile.is_hitman:
            context["form_status"] = FormStatus(object.status)
        if user.profile.is_boss and object.is_new:
            context["form_assigned"] = FormAssigned(user)
        context["avatar_id"] = range(10)
        return context


@login_required
def update_hit(request, pk):
    object = get_object_or_404(Hit, id=pk)
    def show_error(f, request):
        for k, v in f.errors.items():
            messages.error(request, f'{k} {"".join(v)}')

    if request.method == "POST":
        # TODO move this valid to the form
        if request.user == object.assigned and request.user.profile.is_hitman:
            f = FormStatus(object.status, request.POST)
            if f.is_valid():
                object.status = f.cleaned_data.get("change_status")
                object.save()
                messages.success(request, f"Hit status was updated to: {object.get_status()}")
            else:
                show_error(f, request)
        # TODO move this valid to the form
        if request.user.profile.is_boss and object.is_new:
            f = FormAssigned(request.user, request.POST)
            if f.is_valid():
                object.assigned = request.POST.get("assigned")
                object.save()
                messages.success(request, f"Hit assigned was updated to: {object.assigned}")
            else:
                show_error(f, request)
        return redirect(object)
    else:
        raise Http404("wtf!")


class CreateHit(generic.CreateView):
    model = Hit
    fields = ("assigned", "target", "description",)
    
    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        user = self.request.user
        if user.profile.is_hitman:
            raise Http404("is hitman")
        elif user.profile.is_boss:
            form.fields["assigned"].queryset = user.profile.manages.all()
        return form

    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        self.object = object
        messages.success(self.request, "Hit was added")
        return HttpResponseRedirect(self.get_success_url())


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    return render(request, "index.html")

hit_view = login_required(HitView.as_view())
dashboard = login_required(Dashboard.as_view())
create_hit = login_required(CreateHit.as_view())
