from django.shortcuts import render, get_object_or_404
from .models import Property
from  properties.models import Property


def index(request):
    return render(request, 'test.html',{
        "properties": Property.objects.all(),
        })
    #return HttpResponse('Response from property')

def property_view(request):
    properties = Property.objects.all()
    return render(request, 'properties/properties.html', {'properties': properties})

def get_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, 'properties/property_detail.html', {'property': property_obj})

def property_search(request):
    query = request.GET.get("query", "")
    results = []

    if query:
        results = Property.objects.filter(
            title__icontains=query
        )

    return render(request, 'properties/property_search.html', {
        'results': results,
        'query': query
    })