
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from user import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, SellerForm
from django.contrib.auth import get_user_model
from .models import create_seller, Seller
from properties.models import Property
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from offer.models import PurchaseOffer,CreditCardInfo,MortgageInfo
from django.contrib.auth.decorators import login_required

User = get_user_model()

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,('Invalid username or password.'))
            return redirect('user:login')
    else:
        return render(request, 'user/login.html')

def logout_user(request):
    logout(request)
    #messages.success(request,('You have been logged out.'))
    return redirect('home')


def create_user(request):
    form = SignUpForm()
    if request.method == 'POST' or request.method == 'FILES':
        form = SignUpForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfully created your user.'))
            return redirect('home')
        else:
            messages.error(request, 'User creation failed.')
            return redirect('user:createuser')
    else:
        return render(request, 'user/createuser.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,request.FILES or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ('You have successfully updated your account.'))
            #return redirect('home')
        return render(request, 'user/updateuser.html',{'user_form':user_form})
    else:
        messages.success(request, 'You must be logged in to update your account.')
        return render(request, 'user/updateuser.html',{})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST' or request.method == 'FILES':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('You have successfully updated your password.'))
                login(request, current_user)
                return redirect('updateuser')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'user/updatepassword.html',{'form':form})

        return render(request, 'user/updatepassword.html', {})
    else:
        messages.error(request, 'You must be logged in to update your account.')

def seller_profile(request, seller_id):
    seller = get_object_or_404(Seller, user__id=seller_id)
    properties = Property.objects.filter(seller=seller).prefetch_related('images')

    return render(request, 'user/seller_profile.html', {
        'seller': seller,
        'properties': properties,
    })

def update_sellerinfo(request):
    if request.user.is_authenticated:
        current_user = request.user

        try:
            seller, created = Seller.objects.get_or_create(user=current_user)
        except Exception as e:
            print(f'Error fetching or creating seller: {e}')

        seller_form = SellerForm(request.POST or None, instance=seller)

        if seller_form.is_valid():
            seller_form.save()

            messages.success(request, ('You have successfully updated your account.'))
            return redirect('home')
        return render(request, 'user/updatesellerinfo.html',{'user_form':seller_form})
    else:
        messages.success(request, 'You must be logged in to update your account.')
        return render(request, 'user/updatesellerinfo.html',{})

def get_all_offers(offer):
    return {
        'id': offer.id,
        'user_id': offer.user_id,
        'user': str(offer.user) if offer.user else None,
        'property_id': offer.property_id,
        'property': str(offer.property),
        'offer_price': str(offer.offer_price),
        'status': offer.status,
        'status_display': offer.get_status_display(),
        'submitted_at': offer.submitted_at.isoformat() if offer.submitted_at else None,
        'expires_at': offer.expires_at.isoformat() if offer.expires_at else None,
    }

class ListOfOffers(ListView):
    model = PurchaseOffer
    template_name = 'offers/offers_list.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return PurchaseOffer.objects.filter(user=self.request.user)

def get_offer_by_offer_id(request, offer_id):
    offer_obj = get_object_or_404(PurchaseOffer, id=offer_id)
    property_obj = offer_obj.property
    return render(request, 'offers/finalize_offer.html', {
        'property': property_obj,
        'offer': offer_obj
    })

def confirm_offer(request, offer_id):
    offer_obj = get_object_or_404(PurchaseOffer, id=offer_id)
    property_obj = offer_obj.property
    return render(request, 'offers/confirm_offer.html', {
        'property': property_obj,
        'offer': offer_obj
    })


@login_required
def payment_information(request, offer_id):
    offer_obj = get_object_or_404(PurchaseOffer, id=offer_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment')

        # Normalize payment method names
        if payment_method == 'Credit card':
            payment_method = 'Credit Card'
        elif payment_method == 'Bank transfer':
            payment_method = 'Bank Transfer'
        elif payment_method == 'Mortgage':
            payment_method = 'Mortgage'

        # Update the offer with payment method
        offer_obj.payment_method = payment_method
        offer_obj.payment_submitted_at = timezone.now()
        offer_obj.save()  # This line saves the payment method to the offer

        # Redirect based on payment method
        if payment_method == 'Credit Card':
            return redirect('user:creditcard_information', offer_id=offer_obj.id)
        elif payment_method == 'Mortgage':
            return redirect('user:mortgage_information', offer_id=offer_obj.id)
        # Add other payment methods as needed

    context = {
        'offer': offer_obj,
    }
    return render(request, 'offers/finalize_offer.html', context)

@login_required
def creditcard_information(request, offer_id):
    offer_obj = get_object_or_404(PurchaseOffer, id=offer_id)

    if request.method == 'POST':
        if not offer_obj.payment_method:
            offer_obj.payment_method = 'Credit Card'
            offer_obj.payment_submitted_at = timezone.now()
            offer_obj.save()

        # Save credit card details
        card_number = request.POST.get('card-number')
        card_token = 'testtesttest'
        last_four_digits = card_number[-4:] if card_number else ''
        expiry_year = int(request.POST.get('Year'))
        expiry_month = int(request.POST.get('Month'))

        # Create or update credit card info
        credit_card_info, created = CreditCardInfo.objects.get_or_create(
            offer=offer_obj,
            defaults={
                'card_token': card_token,
                'last_four_digits': last_four_digits,
                'expiry_year': expiry_year,
                'expiry_month': expiry_month,
            }
        )

        if not created:
            credit_card_info.card_token = card_token
            credit_card_info.last_four_digits = last_four_digits
            credit_card_info.expiry_year = expiry_year
            credit_card_info.expiry_month = expiry_month
            credit_card_info.save()

        # Redirect to confirmation
        return redirect('user:confirm_offer', offer_id=offer_obj.id)

    context = {
        'offer': offer_obj,
    }
    return render(request, 'offers/finalize_offer.html', context)

@login_required
def mortgage_information(request, offer_id):
    offer_obj = get_object_or_404(PurchaseOffer, id=offer_id)

    if request.method == 'POST':
        # Set payment method on offer if not already set
        if not offer_obj.payment_method:
            offer_obj.payment_method = 'Mortgage'
            offer_obj.payment_submitted_at = timezone.now()
            offer_obj.save()

        # Save mortgage details
        mortgage_number = request.POST.get('card-number')
        bank_name = request.POST.get('bank-name')
        approved_amount = request.POST.get('approved-amount')

        # Convert approved_amount to appropriate format
        if approved_amount:
            try:
                approved_amount = float(approved_amount)
            except ValueError:
                approved_amount = None

        # Create or update mortgage info
        mortinfo, created = MortgageInfo.objects.get_or_create(
            offer=offer_obj,
            defaults={
                'mortgage_number': mortgage_number,
                'bank_name': bank_name,
                'approved_amount': approved_amount
            }
        )

        if not created:
            mortinfo.mortgage_number = mortgage_number
            mortinfo.bank_name = bank_name
            mortinfo.approved_amount = approved_amount
            mortinfo.save()

        # Redirect to confirmation (instead of confirm_offer)
        return redirect('user:confirm_offer', offer_id=offer_obj.id)

    context = {
        'offer': offer_obj,
    }
    return render(request, 'offers/finalize_offer.html', context)

def confirmation(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id)
    return render(request, 'offers/confirmation.html', {'offer': offer})