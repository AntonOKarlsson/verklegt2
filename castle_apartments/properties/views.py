from django.shortcuts import render

from models import Property

from  properties.models import Property


def index(request):
    return render(request, 'test.html',{
        "properties": Property.objects.all(),
        })
    #return HttpResponse('Response from property')

