from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.contrib import messages
from django.http import Http404
from core.models import Hit
import django_tables2 as table
import django_filters
import django_filters.views
from django import forms


class FormStatus(forms.Form):
    change_status = forms.ChoiceField(choices=Hit.CHOICES)

    def __init__(self, actual_status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = Hit.next_status(actual_status)
        self.fields["change_status"].choices = choices


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


class Dashboard(table.SingleTableMixin, django_filters.views.FilterView):
    template_name = "dashboard.html"
    model = Hit
    table_class = HitTable
    filterset_class = HitFilter

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.profile.is_hitman():
            qs = qs.filter(assigned=user)
        return qs


class HitView(generic.DetailView):
    model = Hit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get("object")
        if Hit.next_status(object.status):
            context["form_status"] = FormStatus(object.status)
        context["avatar_id"] = range(11)
        return context


@login_required
def update_hit(request, pk):
    object = get_object_or_404(Hit, id=pk)
    if request.method == "POST" and request.user == object.assigned:
        object.status = request.POST.get("change_status")
        object.save()
        messages.success(request, f"Hit was updated to: {object.get_status()}")
    else:
        raise Http404("not owned")
    return redirect(object)


class CreateHit(generic.CreateView):
    model = Hit
    fields = ("assigned", "target", "description",)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        messages.success(self.request, "Hit was added")
        return super().form_valid(form)


hit_view = login_required(HitView.as_view())
dashboard = login_required(Dashboard.as_view())
create_hit = login_required(CreateHit.as_view())
