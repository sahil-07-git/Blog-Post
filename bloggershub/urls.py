from django.contrib import admin
from django.urls import path, include
from blog.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
]
