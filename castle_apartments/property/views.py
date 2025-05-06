from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from  property.models import Property


def index(request):
    #return render(request, 'test.html',{"properties:" Property.objects.all()} )
    return HttpResponse('Response from property')

