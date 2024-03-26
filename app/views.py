from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic.list import ListView
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