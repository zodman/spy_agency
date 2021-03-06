from django.contrib import admin
from django.urls import path, include
from django.views import generic
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/", include("loginas.urls")),
    path("register/",
         generic.RedirectView.as_view(pattern_name="registration_register")),
    path("logout/",
         generic.RedirectView.as_view(pattern_name="auth_logout")),

    path("hits/", generic.RedirectView.as_view(pattern_name="dashboard")),
    path("hits/bulk", generic.RedirectView.as_view(pattern_name="bulk")),
    path("hitmen/", generic.RedirectView.as_view(pattern_name="hitmen")),
    path("accounts/", include("registration.backends.simple.urls")),
    path("app/", include("core.urls")),
    path("messages/",
         generic.TemplateView.as_view(template_name="messages.html"),
         name="messages"),
    path('', index, name='index'),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
