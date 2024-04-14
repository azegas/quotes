"""
A module that contains all the urls for this project.

A single place from which ALL the urls are created.
"""

from django.contrib import admin
from django.urls import include, path

from project.views import Index, MyRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("rdt", MyRedirectView.as_view(), name="rdt"),
    path("quotes/", include("apps.quotes.urls")),
    path("authors/", include("apps.authors.urls")),
]
