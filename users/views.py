from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserUpdateForm, ProfileUpdateForm, RegisterForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from news.models import Article

# Create your views here.
@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            for user in User.objects.all():
                Profile.objects.get_or_create(user = user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been Created for {username}! You can now log in.')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form":form})

@login_required
@csrf_protect
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect("profile")

    else:
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    user_post = Article.objects.filter(editor=request.user).order_by("-pub_date")
    post = Article.objects.filter(editor=request.user).order_by("-pub_date")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_post": user_post,
        "posts": post
    }

    return render(request, "profile/profile.html", context)