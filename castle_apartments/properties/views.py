from django.shortcuts import render, get_object_or_404
from .models import Property
from  properties.models import Property
from django.http import JsonResponse

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

def json_search(request):
    if 'property_search' in request.GET:
        search_term = request.GET['property_search']

        data = [
            {
                'id': p.id,
                'title': p.title,
                'address': p.address,
                'price': float(p.price),
                'is_sold': p.is_sold,
                'created_at': p.created_at.isoformat(),
            }
            for p in Property.objects.filter(
                title__icontains=search_term
            ).order_by('title')
        ]

        return JsonResponse({'data': data})

    # fallback: return all properties as HTML page
    properties = Property.objects.all()
    return render(request, "properties/properties.html", {"properties": properties})

def property_search_page(request):
    return render(request, 'properties/json_search.html')