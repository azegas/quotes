"""A module for quotes app views."""

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from ag_mixins import AgObjectRetrievalMixin
from apps.quotes.forms import QuoteForm
from apps.quotes.models import Quote

logger = logging.getLogger(__name__)


class QuoteListView(View):
    """
    gCVB example:

    class QuoteListView(ListView):
        model = Quote
        template_name = "quotes/quote_list.html" # default
    """

    template_name = "quotes/quote_list.html"
    partial_template_name = "quotes/partials/quote_list_partial.html"

    def get(self, request):
        """What happens to this view when get request knocks on the door.

        On get request - no parameters are being passed, render all quotes

        """

        logger.info(
            "%s view accessed by user: %s",
            self.__class__.__name__,
            request.user.username,
        )

        quotes = Quote.objects.all()

        return render(request, self.template_name, {"object_list": quotes})

    def post(self, request):
        """What happens to this view when POST request knocks on the door.

        On post request (HTMX requires for search to have a POST request), we
        check if the query parameter q was passed, if yes - render a partial
        template that contains the quotes that match the query.
        """

        query = request.POST.get("q")

        if query:
            # If there's a search query, filter quotes accordingly
            quotes = Quote.objects.filter(text__icontains=query)
        else:
            # If no search query, list all quotes
            quotes = Quote.objects.all()

        return render(
            request, self.partial_template_name, {"object_list": quotes}
        )


class QuoteDetailView(AgObjectRetrievalMixin, View):
    """
    gCVB example:

    class QuoteDetailView(DetailView):
        model = Quote
        template_name = "quotes/quote_detail.html" # default
    """

    template_name = "quotes/quote_detail.html"

    def get(self, request, pk):
        """What happens to this view when get request knocks on the door."""

        quote = self.ag_get_object_by_id(Quote, pk)

        logger.info(
            "%s view of quote (ID: %s) accessed by user: %s",
            self.__class__.__name__,
            quote.pk,
            request.user.username,
        )

        return render(request, self.template_name, {"quote": quote})


class QuoteCreateView(View):
    """
    gCVB example:

    class QuoteCreateView(CreateView):
        model = Quote
        fields = ["text", "author", "active",]
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_form.html" # default
    """

    form_class = QuoteForm
    template_name = "quotes/quote_form.html"
    success_url = reverse_lazy("quote-list")

    def get(self, request):
        """What happens to this view when get request knocks on the door."""

        logger.info(
            "%s view accessed by user: %s",
            self.__class__.__name__,
            request.user.username,
        )

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """
        The post method handles form submission

        1. It creates a form instance populated with request.POST data
        2. checks if the form is valid
        3. saves the form if so
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            # form.save() # would use this if it was a forms.ModelForm
            text = form.cleaned_data["text"]
            author = form.cleaned_data["author"]
            active = form.cleaned_data["active"]
            quote = Quote.objects.create(
                text=text, author=author, active=active
            )
            quote.save()
            logger.info(
                "Quote (ID: %s) created successfully by user: %s",
                quote.pk,
                request.user.username,
            )
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {"form": form})


class QuoteDeleteView(AgObjectRetrievalMixin, View):
    """
    class QuoteDeleteView(DeleteView):
        model = Quote
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_confirm_delete.html" # default
    """

    template_name = "quotes/quote_confirm_delete.html"
    success_url = reverse_lazy("quote-list")

    def get(self, request, pk):
        """What happens to this view when get request knocks on the door."""

        logger.info(
            "%s view accessed by user: %s",
            self.__class__.__name__,
            request.user.username,
        )

        quote = self.ag_get_object_by_id(Quote, pk)
        return render(request, self.template_name, {"object": quote})

    def post(self, _request, pk):
        """
        What happens to this view when post request knocks on the door.

        about _request - _arguments in Python can be named with a leading
        underscore to indicate that they are intentionally unused
        """
        quote = self.ag_get_object_by_id(Quote, pk)

        logger.info(
            "Deleting quote '%s' (ID: %s) by user: %s",
            quote.text,
            quote.pk,
            _request.user.username,
        )

        quote.delete()
        return HttpResponseRedirect(self.success_url)


class QuoteUpdateView(AgObjectRetrievalMixin, View):
    """
    class QuoteUpdateView(UpdateView):
        model = Quote
        fields = "__all__"
        success_url = reverse_lazy('quote-list')
        template_name = "quotes/quote_form.html" # default
    """

    form_class = QuoteForm
    template_name = "quotes/quote_form.html"
    success_url = reverse_lazy("quote-list")

    def get(self, request, pk):
        """What happens to this view when get request knocks on the door."""

        logger.info(
            "%s view accessed by user: %s",
            self.__class__.__name__,
            request.user.username,
        )

        quote = self.ag_get_object_by_id(Quote, pk)
        form = self.form_class(
            initial={
                "text": quote.text,
                "author": quote.author,
                "active": quote.active,
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        """What happens to this view when post request knocks on the door."""
        quote = self.ag_get_object_by_id(Quote, pk)
        form = self.form_class(request.POST)

        if form.is_valid():
            quote.text = form.cleaned_data["text"]
            quote.author = form.cleaned_data["author"]
            quote.active = form.cleaned_data["active"]
            quote.save()
            logger.info(
                "Quote %s updated successfully by user: %s",
                quote.pk,
                request.user.username,
            )
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {"form": form})
