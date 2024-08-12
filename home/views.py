from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if the user is logged in
    return render(request, 'home/index.html')  # Show the homepage if the user is not logged in

@login_required
def dashboard(request):
    return render(request, 'home/dashboard.html')  # Dashboard view for logged-in users

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # Automatically log the user in after registration
            return redirect('dashboard')  # Redirect to the dashboard after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})  # Render the registration page

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})