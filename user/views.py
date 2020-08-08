from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignInForm, SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, "User Registered Successfully!")
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


def login_request(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                next_url = cache.get('next')
                messages.success(request, "Successfully Logged In!")
                if next_url:
                    cache.delete('next')
                    return HttpResponseRedirect(next_url)
                return redirect('core:home')
            else:
                messages.error(request, "Invalid Username or Password!")
        else:
            messages.error(request, "Invalid Username or Password!")
    else:
        cache.set('next', request.GET.get('next', None))
        form = SignInForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "User Logged Out!")
    return redirect('user:login')
