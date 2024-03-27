from django.urls import path
from app.views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("quote-list", QuoteListView.as_view(), name="quote-list"),
    path("author-list", AuthorListView.as_view(), name="author-list"),
    path("quote-list/<int:pk>", QuoteDetailView.as_view(), name="quote-detail"),
    path("author-list/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
]