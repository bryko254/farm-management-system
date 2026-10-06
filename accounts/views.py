import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistrationForm

logger = logging.getLogger(__name__)


def register(request):
    if not settings.ALLOW_REGISTRATION:
        raise Http404
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        logger.info('New user registered: id=%s', user.pk)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')
