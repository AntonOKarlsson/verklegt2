from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from user import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.forms import SignUpForm


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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
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
            messages.success(request, 'Sign up failed.')
            return redirect('create_user')
    else:
        return render(request, 'user/createuser.html',{'form':form})



