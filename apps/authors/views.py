"""A module for author app views."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_context_data(self, **kwargs):
        """Add the author's quotes to the context"""
        context = super().get_context_data(**kwargs)
        context["quotes"] = self.object.quotes.all()
        return context


# CreateView is very similar to FormView, but use CreateView anyway, it must be
# there for a reason
# does some additional magic for us, like saving to the db
# YT - "Learn Django Class Based Views - CreateView - Theory and Examples"
class AuthorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Generic CBV view for author create page"""

    model = Author
    fields = [
        "name",
        "lastname",
    ]
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_form.html"  # default

    def test_func(self):
        """Checks if the user is a superuser."""
        return self.request.user.is_superuser


class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Generic CBV view for author delete page"""

    model = Author
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_confirm_delete.html"  # default

    def test_func(self):
        """Checks if the user is a superuser."""
        return self.request.user.is_superuser


class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Generic CBV view for author update page"""

    model = Author
    fields = "__all__"
    success_url = reverse_lazy("author-list")
    template_name = "authors/author_form.html"  # default

    def test_func(self):
        """Checks if the user is a superuser."""
        return self.request.user.is_superuser
