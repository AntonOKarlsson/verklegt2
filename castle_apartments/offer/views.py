from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from properties.models import Property
from .models import PurchaseOffer
from django.utils import timezone
from datetime import timedelta
from offer.models import PurchaseOffer

def offer_on_property_by_id(request, id):
    property_obj = get_object_or_404(Property, id=id)
    if request.method == 'POST':
        try:
            offer_price = request.POST.get('offer_price')

            # Create the offer without a user initially
            offer = PurchaseOffer(
                property=property_obj.id,
                offer_price=offer_price,
                expires_at=timezone.now() + timedelta(days=14)
            )

            # Assign the user only if authenticated
            if request.user.is_authenticated:
                offer.user = request.user

            # Save the offer
            offer.save()

            messages.success(request, "Your offer has been submitted successfully!")
            return redirect('property-by-id', id=id)

        except Exception as e:
            print("Error:", str(e))
            messages.error(request, f"Error submitting offer: {str(e)}")
            return render(request, 'offers/offer_form.html', {
                'property': property_obj,
                'error': str(e)
            })

    return render(request, 'offers/offer_form.html', {'property': property_obj})




# Create your views here.
