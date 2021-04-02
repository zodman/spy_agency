from django.urls import path, include
from django.conf import settings
from .views import dashboard

urlpatterns = [
        path("dashboard", dashboard, name="dashboard"),
]

