from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignInForm, SignUpForm, ProfileForm
from .models import User
from quiz.models import UserResponse, Question, Option


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


def profile(request, username=None):
    user = User.objects.get(username=username)
    user_response = UserResponse.objects.filter(user=user).select_related('quiz_exam')
    if request.method == 'POST':
        form = ProfileForm(user, request.POST, request.FILES)
        if form.is_valid():
            form.save(user=user)
            messages.success(request, "Profile Updated Successfully!")
            return HttpResponseRedirect(reverse('user:profile', kwargs={'username': username}))
    else:
        form = ProfileForm(user)
    return render(request, 'user/profile.html', {'form': form, 'user': user, 'user_response': user_response})


def quiz_result(request, quiz_exam=None):
    context = {}
    try:
        user_response = UserResponse.objects.get(
            user=request.user, quiz_exam_id=quiz_exam)
    except:
        user_response = None
    if user_response:
        questions = Question.objects.filter(id__in=user_response.response.keys()).prefetch_related('options')
        context['user_response'] = user_response
        context['response'] = zip(questions, user_response.response.values())
    return render(request, 'user/quiz-result.html', context=context)
