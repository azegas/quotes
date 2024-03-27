from django.urls import path
from app.views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("quote-list", QuoteListView.as_view(), name="quote-list"),
    path("author-list", AuthorListView.as_view(), name="author-list"),
    path("quote-list/<int:pk>", QuoteDetailView.as_view(), name="quote-detail"),
    path("author-list/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("quote-list/create", QuoteCreateView.as_view(), name="quote-create"),
    path("author-list/create", AuthorCreateView.as_view(), name="author-create"),
    path("quote-list/<int:pk>/delete", QuoteDeleteView.as_view(), name="quote-delete"),
    path("author-list/<int:pk>/delete", AuthorDeleteView.as_view(), name="author-delete"),
]