import random
import string
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from ads.models import Ad, Response

logger = logging.getLogger(__name__)

def generate_confirmation_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_confirmed = False
            user.confirmation_code = generate_confirmation_code()
            user.save()
            try:
                send_mail(
                    'Confirm your email',
                    f'Please confirm your email by using this code: {user.confirmation_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f'Error sending email: {e}')
            return redirect('confirm_email', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def confirm_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.confirmation_code:
            user.email_confirmed = True
            user.confirmation_code = ''
            user.save()
            login(request, user)
            return redirect('category_list')
    return render(request, 'users/confirm_email.html', {'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    Ad.objects.filter(author=user).update(author=None)
    Response.objects.filter(author=user).update(author=None)
    user.delete()
    messages.success(request, 'User and all related records have been deleted.')
    return redirect('admin:users_customuser_changelist')
