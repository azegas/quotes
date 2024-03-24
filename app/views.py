from django.shortcuts import render, HttpResponse
from django.views import View



class Index(View):
    def get(self, request):
        print("get")
        return HttpResponse("Welcome to quotes app")

    # make sure to comment out the csfr middleware for this to work
    def post(self, request):
        print("posted")
        return HttpResponse("someone has posted")