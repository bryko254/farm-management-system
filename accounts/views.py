from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"New user registered: {user.username}")
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logger.info(f"User {request.user.username} logging out")
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        logger.info("User logged out successfully")
        return redirect('home')
    else:
        logger.warning(f"Logout attempted with GET request by {request.user.username}")
        return redirect('home')
