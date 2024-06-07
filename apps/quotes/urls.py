"""A module that contains all the urls for the quote app."""

from django.urls import path

from apps.quotes.views import (
    QuoteCreateView,
    QuoteDeleteView,
    QuoteDetailView,
    QuoteListView,
    QuoteUpdateView,
)

urlpatterns = [
    path("list", QuoteListView.as_view(), name="quote-list"),
    path("detail/<int:pk>", QuoteDetailView.as_view(), name="quote-detail"),
    path("create/", QuoteCreateView.as_view(), name="quote-create"),
    path(
        "delete/<int:pk>",
        QuoteDeleteView.as_view(),
        name="quote-delete",
    ),
    path(
        "update/<int:pk>",
        QuoteUpdateView.as_view(),
        name="quote-update",
    ),
]
