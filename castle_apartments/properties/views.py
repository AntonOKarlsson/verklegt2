from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PropertyForm, PropertyImageFormSet
from .models import Property, PostalCode
from offer.models import PurchaseOffer
from property_images.models import PropertyImage

def property_view(request):
    thumbnail_qs = PropertyImage.objects.filter(is_thumbnail=True)

    properties = Property.objects.all().prefetch_related(
        Prefetch('images', queryset=thumbnail_qs, to_attr='prefetched_thumbnails')
    ).select_related('seller__user')

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
def add_property2(request):
    if request.method == 'POST':
        property_form2 = PropertyForm(request.POST, request.FILES)

        files = request.FILES.getlist('files')
        file_list = []

        if property_form2.is_valid():
            prop = property_form2.save(commit=False)
            prop.seller = request.user.seller_profile
            prop.save()
            first = True

            for file in files:
                if first:
                    PropertyImage.objects.create(property=prop, image=file, is_thumbnail=True)
                    first = False
                else:
                    PropertyImage.objects.create(property=prop, image=file)


        return redirect('properties')

    else:
        property_form2 = PropertyForm()


    return render(request, 'properties/add_property.html', {
        'property_form': property_form2,
    })



@login_required
def add_property(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        image_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if property_form.is_valid() and image_formset.is_valid():
            prop = property_form.save(commit=False)
            prop.seller = request.user.seller_profile
            prop.save()

            for form in image_formset.cleaned_data:
                if form and form.get('image'):
                    PropertyImage.objects.create(
                        property=prop,
                        image=form['image'],
                        is_thumbnail=form.get('is_thumbnail', False)
                    )

            return redirect('properties')

    else:
        property_form = PropertyForm()
        image_formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'properties/add_property.html', {
        'property_form': property_form,
        'image_formset': image_formset
    })

def search_properties(request):
    search_term = request.GET.get('search_term', '').strip()
    postal_code = request.GET.get('postal_code')
    price_range = request.GET.get('price_range')
    property_type = request.GET.get('property_type')
    size_range = request.GET.get('size_range')
    room_range = request.GET.get('room_range')
    order_by = request.GET.get('order_by')

    if request.GET:
        results = Property.objects.filter(is_sold=False)
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

    if size_range:
        if '+' in size_range:
            try:
                min_size = int(size_range.replace('+', ''))
                results = results.filter(size_sqm__gte=min_size)
            except ValueError:
                pass
        else:
            try:
                min_size, max_size = map(int, size_range.split('-'))
                results = results.filter(size_sqm__gte=min_size, size_sqm__lte=max_size)
            except ValueError:
                pass

    if room_range:
        if '+' in room_range:
            try:
                min_rooms = int(room_range.replace('+', ''))
                results = results.filter(num_rooms__gte=min_rooms)
            except ValueError:
                pass
        elif '-' in room_range:
            try:
                min_rooms, max_rooms = map(int, room_range.split('-'))
                results = results.filter(num_rooms__gte=min_rooms, num_rooms__lte=max_rooms)
            except ValueError:
                pass
        else:
            try:
                exact_rooms = int(room_range)
                results = results.filter(num_rooms=exact_rooms)
            except ValueError:
                pass

    if order_by in ['title', '-title', 'price', '-price']:
        results = results.order_by(order_by)

    # ✅ Prefetch thumbnails and seller.user
    thumbnail_qs = PropertyImage.objects.filter(is_thumbnail=True)
    results = results.prefetch_related(
        Prefetch('images', queryset=thumbnail_qs, to_attr='prefetched_thumbnails')
    ).select_related('seller__user')

    return render(request, 'properties/property_search.html', {
        'properties': results,
        'postal_codes': PostalCode.objects.all(),
        'property_types': Property.objects.values_list('property_type', flat=True).distinct(),
    })

def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.user != property.seller.user:
        return HttpResponseForbidden("You don't have permission to edit this property.")

    form = PropertyForm(request.POST or None, request.FILES or None, instance=property)

    if request.method == 'POST' and form.is_valid():
        form.save()

        images = request.FILES.getlist('images')
        for image in images:
            PropertyImage.objects.create(property=property, image=image)

        return redirect('user:seller-profile', property.seller.id)

    return render(request, 'properties/edit_property.html', {
        'form': form,
        'property': property
    })

def set_thumbnail(request, image_id):
    image = get_object_or_404(PropertyImage, id=image_id)
    property = image.property

    if property.seller.user != request.user:
        return HttpResponseForbidden("You do not own this property.")

    PropertyImage.objects.filter(property=property).update(is_thumbnail=False)

    image.is_thumbnail = True
    image.save()

    return redirect('edit_property', property.id)