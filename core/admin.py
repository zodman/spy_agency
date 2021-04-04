from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin

from .models import Hit, Profile

class ProfileAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ("id", "user_link", "type")
    change_links = ("user",)
    filter_horizontal = ("manages",)

admin.site.register(Hit)
admin.site.register(Profile, ProfileAdmin)
