"""
A module that contains all the urls for this project.

A single place from which ALL the urls are created.
"""

from django.contrib import admin
from django.urls import include, path

from project.views import Index, RandomQuote

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", Index.as_view(), name="index"),
    path("random-quote", RandomQuote.as_view(), name="random-quote"),
    path("quotes/", include("apps.quotes.urls")),
    path("authors/", include("apps.authors.urls")),
]
