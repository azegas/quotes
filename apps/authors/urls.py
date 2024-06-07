"""A module that contains all the urls for the author app."""

from django.urls import path

from apps.authors.views import (
    AuthorCreateView,
    AuthorDeleteView,
    AuthorDetailView,
    AuthorListView,
    AuthorUpdateView,
)

urlpatterns = [
    path("list", AuthorListView.as_view(), name="author-list"),
    path("detail/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("create", AuthorCreateView.as_view(), name="author-create"),
    path("delete/<int:pk>", AuthorDeleteView.as_view(), name="author-delete"),
    path("update/<int:pk>", AuthorUpdateView.as_view(), name="author-update"),
]
