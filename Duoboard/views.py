from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You have arrived at the Duoboard index.")

# Create your views here.
