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
            return redirect('login')

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
            return redirect('create_user')
    else:
        return render(request, 'user/createuser.html',{'form':form})

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






