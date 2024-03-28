from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import RedirectView


class Index(View):
    def get(self, request):
        message = "ROFL"
        return render(request,"project/index.html", {"message" : message})

    # make sure to comment out the csfr middleware for this to work
    def post(self, request):
        print("posted")
        return HttpResponse("someone has posted")
    
class RedirectView(RedirectView):
    url = "https://www.youtube.com"