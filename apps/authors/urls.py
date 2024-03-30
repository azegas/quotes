"""A module that contains all the urls for the author app."""

from django.urls import path
from apps.authors.views import (
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorDeleteView,
    AuthorUpdateView,
)

urlpatterns = [
    path("list", AuthorListView.as_view(), name="author-list"),
    path("detail/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("create", AuthorCreateView.as_view(), name="author-create"),
    path("<int:pk>/delete", AuthorDeleteView.as_view(), name="author-delete"),
    path("<int:pk>/update", AuthorUpdateView.as_view(), name="author-update"),
]
