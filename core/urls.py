from django.urls import path, include
from django.conf import settings
from .views import dashboard, hit_view, update_hit
from .views import create_hit

urlpatterns = [
    path("hits", dashboard, name="dashboard"),
    path("hit/create", create_hit, name="create_hit"),
    path("hit/u/<int:pk>", update_hit, name="update_hit"),
    path("hit/<int:pk>", hit_view, name="hit_view"),
]

