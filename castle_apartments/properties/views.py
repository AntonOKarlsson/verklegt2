from django.shortcuts import render, get_object_or_404
from .models import Property
from  properties.models import Property
from django.http import JsonResponse
from property_images.models import PropertyImage


def property_view(request):
    properties = Property.objects.all()

    return render(request, 'properties/properties.html', {'properties': properties})


def get_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, 'properties/property_detail.html', {'property': property_obj})


def offer_on_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)
    property_images = property_obj.images.all()  # Get the property images

    # Add context for the template
    context = {
        'property': property_obj,
        'property_images': property_images,
    }

    return render(request, 'offers/offer_form.html', context)

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
    min_size = request.GET.get('min_size')
    max_size = request.GET.get('max_size')
    property_type = request.GET.get('property_type')

    results = Property.objects.all()

    if search_term:
        results = results.filter(title__icontains=search_term)

    if postal_code:
        results = results.filter(postal_code__icontains=postal_code)

    if min_price:
        results = results.filter(price__gte=int(min_price))

    if max_price:
        results = results.filter(price__lte=int(max_price))

    if min_size:
        results = results.filter(size_sqm__gte=int(min_size))

    if max_size:
        results = results.filter(size_sqm__lte=int(max_size))

    if property_type:
        results = results.filter(property_type__iexact=property_type)

    ordering = request.GET.get('ordering')
    if ordering in ['price', '-price', 'title', '-title']:
        results = results.order_by(ordering)

    data = [
        {
            'id': p.id,
            'title': p.title,
            'address': p.address,
            'price': float(p.price),
            'size_sqm': float(p.size_sqm) if p.size_sqm is not None else None,
            'num_rooms': p.num_rooms,
            'is_sold': p.is_sold,
            'thumbnail_url': p.images.filter(is_thumbnail=True).first().image.url
            if p.images.filter(is_thumbnail=True).exists() else None,
        }
        for p in results
    ]

    return JsonResponse({'data': data})