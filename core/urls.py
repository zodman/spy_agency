from django.urls import path
from .views import dashboard, hit_view, update_hit
from .views import create_hit, manages, bulk, hitmen, hitman_detail
from .views import hitman_update

urlpatterns = [
    path('hitmen/manage', manages, name="manage"),
    path('hitmen/<int:pk>',hitman_detail, name="hitman_detail"),
    path('hitmen/u/<int:pk>',hitman_update, name="hitman_update"),
    path('hitmen/',hitmen, name="hitmen"),
    path("hit/create", create_hit, name="create_hit"),
    path("hit/u/<int:pk>", update_hit, name="update_hit"),
    path("hit/<int:pk>", hit_view, name="hit_view"),
    path("hits/bulk",bulk, name="bulk"),
    path("hits", dashboard, name="dashboard"),

]

