from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
 # Ensure you import your Notes model

# Registration view for user signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})

# Login view for users and superusers
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect superuser (admin) to the admin dashboard
            if user.is_superuser:
                return redirect('admin_dashboard')  # Change this to your admin dashboard URL
            # Redirect regular user to the notes list
            return redirect('notes.list')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'home/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Welcome/home view
def home(request):
    return render(request, 'home/welcome.html')
