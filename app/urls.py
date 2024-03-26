from django.urls import path
from app.views import Index, QuoteListView, AuthorListView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("quote-list", QuoteListView.as_view(), name="quote-list"),
    path("author-list", AuthorListView.as_view(), name="author-list"),
]