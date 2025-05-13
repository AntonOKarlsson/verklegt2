from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PropertyForm
from .models import Property, PostalCode
from offer.models import PurchaseOffer
from property_images.models import PropertyImage

def property_view(request):
    properties = Property.objects.all()

    return render(request, 'properties/properties.html', {'properties': properties})


def get_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, 'properties/property_detail.html', {'property': property_obj})

@login_required
def offer_on_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)

    if request.method == 'POST':
        offer_price_str = request.POST.get('offer_price')

        try:
            offer_price = Decimal(offer_price_str)
        except (TypeError, InvalidOperation):
            messages.error(request, "Invalid offer price.")
            return redirect('property-by-id', id=id)

        offer = PurchaseOffer(
            user=request.user,
            property=property_obj,
            offer_price=offer_price,
            expires_at=timezone.now() + timedelta(days=14)
        )

        offer.save()
        messages.success(
            request,
            f"""🎯 Your offer was submitted successfully!

        🏠 Property: {property_obj.title}
        💸 Your offer: ISK {offer_price:,.2f}
        ⏳ Expires: {offer.expires_at.strftime('%B %d, %Y')}

        You will be notified as soon as the seller responds!"""
        )

        return redirect('property-by-id', id=id)

    property_images = property_obj.images.all()
    context = {
        'property': property_obj,
        'property_images': property_images,
    }
    return render(request, 'offers/offer_form.html', context)

from django.http import JsonResponse
from .models import Property


@login_required
def add_property(request):
    property_form=PropertyForm()
    if not request.user.is_seller:
        messages.error(request, "You must be a seller to add a property.")
        return redirect('home')

    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)

        if property_form.is_valid():
            property_form.save()
            messages.success(request, 'Property added successfully.')
            return redirect('home')

    return render(request, 'properties/add_property.html', {'property_form':property_form})

def search_properties(request):
    search_term = request.GET.get('search_term', '').strip()
    postal_code = request.GET.get('postal_code')
    price_range = request.GET.get('price_range')
    property_type = request.GET.get('property_type')
    order_by = request.GET.get('order_by')

    has_filters = any([
        search_term, postal_code, price_range, property_type, order_by
    ])

    if request.GET:
        results = Property.objects.all()
    else:
        results = Property.objects.none()

    if search_term:
        results = results.filter(
            Q(title__icontains=search_term) | Q(address__icontains=search_term)
        )

    if postal_code:
        results = results.filter(postal_code=postal_code)

    if price_range:
        if '+' in price_range:
            try:
                min_price = int(price_range.replace('+', ''))
                results = results.filter(price__gte=min_price)
            except ValueError:
                pass
        else:
            try:
                min_price, max_price = map(int, price_range.split('-'))
                results = results.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                pass

    if property_type:
        results = results.filter(property_type__iexact=property_type)

    if order_by in ['title', '-title', 'price', '-price']:
        results = results.order_by(order_by)

    return render(request, 'properties/property_search.html', {
        'properties': results,
        'postal_codes': PostalCode.objects.all(),
        'property_types': Property.objects.values_list('property_type', flat=True).distinct(),
    })