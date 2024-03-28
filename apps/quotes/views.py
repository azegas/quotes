from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.quotes.models import Quote

class QuoteListView(ListView):
    model = Quote
    template_name = "quotes/quote_list.html" # default

class QuoteDetailView(DetailView):
    model = Quote
    template_name = "quotes/quote_detail.html" # default

# CreateView is very similar to FormView, but use CreateView anyway, it is there for a reason
# does some additional magic for us, like saving to the db
# https://www.youtube.com/watch?v=nW-srV0kKKk&list=PLOLrQ9Pn6caxNb9eFZJ6LfY29nZkKmmXT&index=6&ab_channel=VeryAcademy
class QuoteCreateView(CreateView):
    model = Quote
    fields = ["text", "author", "active",]
    success_url = reverse_lazy('quote-list')
    template_name = "quotes/quote_form.html" # default

class QuoteDeleteView(DeleteView):
    model = Quote
    success_url = reverse_lazy('quote-list')
    template_name = "quotes/quote_confirm_delete.html" # default

class QuoteUpdateView(UpdateView):
    model = Quote
    fields = "__all__"
    success_url = reverse_lazy('quote-list')
    template_name = "quotes/quote_form.html" # default
