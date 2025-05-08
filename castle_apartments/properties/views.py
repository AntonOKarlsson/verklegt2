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

def property_search_page(request):
    postal_codes = Property.objects.values_list('postal_code', flat=True).distinct().order_by('postal_code')
    property_types = Property.objects.values_list('property_type', flat=True).distinct().order_by('property_type')
    return render(request, 'properties/json_search.html', {
        'postal_codes': postal_codes,
        'property_types': property_types
    })


def json_search(request):
    search_term = request.GET.get('property_search', "")
    postal_code = request.GET.get('postal_code')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    property_type = request.GET.get('property_type')

    print("DEBUG: search_term =", search_term,
          "| postal_code =", postal_code,
          "| min_price =", min_price,
          "| max_price =", max_price,
          "| property_type =", property_type)

    results = Property.objects.all()

    if search_term:
        results = results.filter(title__icontains=search_term)

    if postal_code:
        results = results.filter(postal_code__icontains=postal_code)

    if min_price:
        results = results.filter(price__gte=int(min_price))

    if max_price:
        results = results.filter(price__lte=int(max_price))

    if property_type:
        results = results.filter(property_type__iexact=property_type)

    data = [
        {
            'id': p.id,
            'title': p.title,
            'address': p.address,
            'price': float(p.price),
            'is_sold': p.is_sold,
        }
        for p in results
    ]

    return JsonResponse({'data': data})