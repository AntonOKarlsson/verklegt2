from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from properties.models import Property


def home(request):
    return render(request,'home.html')

def about_view(request):
    return render(request, 'about.html')

def financing_view(request):
    return render(request, 'financing.html')

def contact_view(request):
    return render(request, 'contact.html')