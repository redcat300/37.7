from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription
from django.contrib.auth.decorators import login_required

@login_required
def subscribe(request, category):
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        category=category,
        defaults={'email': request.user.email, 'subscribed': True}
    )
    if not created:
        subscription.subscribed = True
        subscription.save()
    send_mail(
        'Subscription Confirmation',
        f'You have successfully subscribed to our newsletter for the category: {category}!',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )
    return redirect('subscription_success')

@login_required
def unsubscribe(request, category):
    subscription = get_object_or_404(Subscription, user=request.user, category=category)
    subscription.subscribed = False
    subscription.save()
    return redirect('unsubscription_success')

def subscription_success(request):
    return render(request, 'newsletter/subscription_success.html')

def unsubscription_success(request):
    return render(request, 'newsletter/unsubscription_success.html')

@login_required
def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipients = Subscription.objects.filter(subscribed=True).values_list('email', flat=True)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
        return redirect('newsletter_success')
    return render(request, 'newsletter/send_newsletter.html')
