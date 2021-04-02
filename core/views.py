from django.views import generic
from core.models import Hit
import django_tables2 as table
import django_filters
import django_filters.views


class HitFilter(django_filters.FilterSet):

    class Meta:
        model = Hit
        fields = "__all__"


class HitTable(table.Table):
    actions = table.TemplateColumn(template_name="_column_actions.html")

    class Meta:
        model = Hit
        exclude = ("description",)


class Dashboard(table.SingleTableMixin, django_filters.views.FilterView):
    template_name = "dashboard.html"
    model = Hit
    table_class = HitTable
    filterset_class = HitFilter


class HitView(generic.DetailView):
    model = Hit


hit_view = HitView.as_view()
dashboard = Dashboard.as_view()
