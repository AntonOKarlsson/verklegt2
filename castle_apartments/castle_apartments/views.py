from django.http import HttpResponse
from django.shortcuts import render
from properties.models import Property

def home(request):
    return render(request,'home.html')