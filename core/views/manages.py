from django.views import generic
from ..forms import FormUsers
from django.contrib.auth.decorators import login_required


class ManageHitman(generic.FormView):
    form_class = FormUsers


manages = login_required(ManageHitman.as_view())

