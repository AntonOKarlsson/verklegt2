from django.http import HttpResponse
from django.shortcuts import render
from properties.models import Property

def home(request):
    return HttpResponse("<h1>Welcome to Castle Apartments</h1>")

def test_view(request):
    properties = Property.objects.all()
    return render(request, 'test.html', {'properties': properties})