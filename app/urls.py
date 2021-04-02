from django.contrib import admin
from django.urls import path, include
from django.views import generic
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/", include("loginas.urls")),
    path("register/", generic.RedirectView.as_view(pattern_name="registration_register")),
    path("accounts/", include("registration.backends.simple.urls")),
    path("app/", include("core.urls")),
    path('', generic.TemplateView.as_view(template_name="index.html"),name='index'),

] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
