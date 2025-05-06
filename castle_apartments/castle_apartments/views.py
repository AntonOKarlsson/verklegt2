from django.http import HttpResponse
from django.shortcuts import render
from properties.models import Property

def home(request):
    return render(request,'home.html')

def test_view(request):
    properties = Property.objects.all()
    return render(request, 'test.html', {'properties': properties})

def property_view(request):
    properties = Property.objects.all()
    return render(request, 'test.html', {'properties': properties})

# def test_isk(value):
#     try:
#         value = float(value)
#         return f"{value:,.0f}".replace(",", ".")
#     except (ValueError, TypeError):
#         return "0"
