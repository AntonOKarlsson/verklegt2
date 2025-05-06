from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Response from castle app')

def test_view(request):
    return render (request, 'test.html')