"""
A module that contains all the urls for this project.

A single place from which ALL the urls are created.
"""

from django.contrib import admin
from django.urls import include, path

from project.views import Index, RandomQuote
from apps.dashboard.views import profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", profile, name="profile"),
    path("", Index.as_view(), name="index"),
    path("random-quote", RandomQuote.as_view(), name="random-quote"),
    path("quotes/", include("apps.quotes.urls")),
    path("authors/", include("apps.authors.urls")),
]
