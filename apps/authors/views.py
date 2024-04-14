"""A module for author app views."""

from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.authors.models import Author


class AuthorListView(ListView):
    """Generic CBV view for author list page"""

    model = Author
    template_name = "authors/author_list.html"  # default


class AuthorDetailView(DetailView):
    """Generic CBV view for author detail page"""

    model = Author
    template_name = "authors/author_detail.html"  # default


# CreateView is very similar to FormView, but use CreateView anyway, it is there for a reason
# does some additional magic for us, like saving to the db
# https://www.youtube.com/watch?v=nW-srV0kKKk&list=PLOLrQ9Pn6caxNb9eFZJ6LfY29nZkKmmXT&index=6&ab_channel=VeryAcademy
class AuthorCreateView(CreateView):
    """Generic CBV view for author create page"""

    model = Author
    fields = [
        "name",
        "lastname",
    ]
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_form.html"  # default


class AuthorDeleteView(DeleteView):
    """Generic CBV view for author delete page"""

    model = Author
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_confirm_delete.html"  # default


class AuthorUpdateView(UpdateView):
    """Generic CBV view for author update page"""

    model = Author
    fields = "__all__"
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_form.html"  # default
