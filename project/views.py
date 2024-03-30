"""A module for project views. Currently have only index."""

from django.shortcuts import render
from django.views import View
from django.views.generic import RedirectView


class Index(View):
    """
    Renders an index page.
    """

    def get(self, request):
        """
        What happens when GET method knocks on this view's door.
        """
        message = "ROFL"
        return render(request, "project/index.html", {"message": message})


class MyRedirectView(RedirectView):
    """
    Does this and that.
    """

    url = "https://www.youtube.com"
