from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from app.models import Quote, Author


class Index(View):
    def get(self, request):
        message = "ROFL"
        return render(request,"index.html", {"message" : message})

    # make sure to comment out the csfr middleware for this to work
    def post(self, request):
        print("posted")
        return HttpResponse("someone has posted")
    

class QuoteListView(ListView):
    model = Quote

class AuthorListView(ListView):
    model = Author

class QuoteDetailView(DetailView):
    model = Quote

class AuthorDetailView(DetailView):
    model = Author


# CreateView is very similar to FormView, but use CreateView anyway, it is there for a reason
# does some additional magic for us, like saving to the db
# https://www.youtube.com/watch?v=nW-srV0kKKk&list=PLOLrQ9Pn6caxNb9eFZJ6LfY29nZkKmmXT&index=6&ab_channel=VeryAcademy
class QuoteCreateView(CreateView):
    model = Quote
    fields = ["text", "author", "active",]
    success_url = '/quote-list'

class AuthorCreateView(CreateView):
    model = Author
    fields = ["name", "lastname",]
    success_url = '/author-list'