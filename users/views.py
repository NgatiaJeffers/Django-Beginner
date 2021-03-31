from django.shortcuts import render, redirect
from django.contrib import messages
from .form import RegisterForm
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account has been Created! You can now log in.')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form":form})