from django.urls import path, include
from django.conf import settings
from .views import dashboard, hit_view

urlpatterns = [
    path("hits", dashboard, name="dashboard"),
    path("hit/<int:pk>", hit_view, name="hit_view"),
]

