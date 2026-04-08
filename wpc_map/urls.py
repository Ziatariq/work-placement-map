from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include("core.admin_urls")),
    path("auth/", include("accounts.urls")),
    path("facilities/", include("facilities.urls")),
    path("", include("core.urls")),
]
