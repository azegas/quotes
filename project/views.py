"""A module for project views. Currently have only index."""

import logging
import secrets

from django.shortcuts import render
from django.views import View

from apps.quotes.models import Quote

logger = logging.getLogger(__name__)


class Index(View):
    """
    Renders an index page.
    """

    def get(self, request):
        """
        What happens when GET method knocks on this view's door.
        """

        logger.info("Index view accessed by user: %s", request.user.username)

        show_random_quote_generator = False

        all_quotes = Quote.objects.all()
        all_quotes_count = len(all_quotes)

        if all_quotes_count >= 3:
            show_random_quote_generator = True

        return render(
            request,
            "project/index.html",
            {
                "all_quotes_count": all_quotes_count,
                "show_random_quote_generator": show_random_quote_generator,
            },
        )


class RandomQuote(View):
    """A view for generating a random quote"""

    def get(self, request):
        """What happens when GET method knocks on this view's door.
        What happens in this case, we take a random quote and pass it to the
        view. And the view is quite simple, displays only the necessary info
        about the chosen quote.

        This info about the quote is later rendered with htmx in a template.
        """

        logger.info(
            "Random quote has been requested by the user: %s",
            request.user.username,
        )

        all_quotes = Quote.objects.all()

        if not all_quotes:
            # Handle the case when there are no quotes in the database
            return render(request, "project/partials/no_quotes.html")

        # using secrets here, because 'bandit' pre-commmit hooks warms me that
        # 'random' package is not safe (Issue: [B311:blacklist])
        random_quote = secrets.choice(all_quotes)

        return render(
            request,
            "project/partials/random_quote.html",
            {"random_quote": random_quote},
        )
