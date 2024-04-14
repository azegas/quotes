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
    path("detail/<int:pk>/delete", QuoteDeleteView.as_view(), name="quote-delete"),
    path("detail/<int:pk>/update", QuoteUpdateView.as_view(), name="quote-update"),
]
