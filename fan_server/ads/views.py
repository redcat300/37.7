import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AdForm, ResponseForm
from .models import Ad, Response, CATEGORY_CHOICES, Comment, Like
from .forms import CommentForm, EditCommentForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from newsletter.models import Subscription

def category_list(request):
    categories = [choice[0] for choice in CATEGORY_CHOICES]
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user, subscribed=True).values_list('category', flat=True)
    return render(request, 'ads/category_list.html', {'categories': categories, 'user_subscriptions': user_subscriptions})

def category_ads(request, category):
    ads = Ad.objects.filter(category=category)
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user, subscribed=True).values_list('category', flat=True)
    return render(request, 'ads/category_ads.html', {'ads': ads, 'category': category, 'user_subscriptions': user_subscriptions})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('category_ads', category=ad.category)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    comments = ad.comments.all()
    comment_form = CommentForm()
    response_form = ResponseForm()
    if request.method == 'POST':
        if 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ad = ad
                comment.author = request.user
                comment.save()
                return redirect('ad_detail', ad_id=ad.id)
        else:
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.ad = ad
                response.author = request.user
                response.save()
                return redirect('ad_detail', ad_id=ad.id)
    return render(request, 'ads/ad_detail.html', {
        'ad': ad,
        'comments': comments,
        'comment_form': comment_form,
        'response_form': response_form,
    })
@login_required
def create_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()
            # Notify ad author
            send_mail(
                'New response to your ad',
                'You have a new response to your ad.',
                settings.DEFAULT_FROM_EMAIL,
                [ad.author.email],
                fail_silently=False,
            )
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ResponseForm()
    return render(request, 'ads/create_response.html', {'form': form})

@login_required
def add_comment(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.author = request.user
            comment.save()


            if ad.author.email and ad.author != request.user:  # Проверяем, что автор объявления не является автором комментария
                send_mail(
                    'New comment on your ad',
                    f'You have a new comment on your ad "{ad.title}".',
                    settings.DEFAULT_FROM_EMAIL,
                    [ad.author.email],
                    fail_silently=False,
                )

            return redirect('category_ads', category=ad.category)
    else:
        form = CommentForm()
    return render(request, 'ads/add_comment.html', {'form': form, 'ad': ad})


@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user or timezone.now() > comment.created_at + timezone.timedelta(hours=1):
        return JsonResponse({'success': False, 'error': 'Permission denied.'})

    form = EditCommentForm(request.POST, request.FILES, instance=comment)
    if form.is_valid():
        form.save()
        response_data = {
            'success': True,
            'author': comment.author.username,
            'content': comment.content,
        }
        if comment.image:
            response_data['image'] = comment.image.url
        if comment.video:
            response_data['video'] = comment.video.url
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form.'})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or comment.ad.author == request.user:
        comment.delete()
        return redirect('ad_detail', ad_id=comment.ad.id)
    else:
        return redirect('ad_detail', ad_id=comment.ad.id)


@login_required
def toggle_like(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    like = Like.objects.filter(ad=ad, user=request.user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(ad=ad, user=request.user)
    return redirect('category_ads', category=ad.category)

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.author == request.user:
        ad.delete()
    return redirect('category_ads', category=ad.category)

@login_required
def user_ads(request):
    ads = Ad.objects.filter(author=request.user)
    for ad in ads:
        ad.response_count = ad.comments.count()
    return render(request, 'ads/user_ads.html', {'ads': ads})

@login_required
def ad_responses(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    responses = ad.comments.all()
    return render(request, 'ads/ad_responses.html', {'ad': ad, 'responses': responses})


@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    if response.ad.author == request.user:
        response.accepted = True
        response.save()
        # Отправка уведомления
        send_mail(
            'Your response was accepted',
            f'Your response to the ad "{response.ad.title}" was accepted.',
            settings.DEFAULT_FROM_EMAIL,
            [response.author.email],
            fail_silently=False,
        )
    return redirect('private_page')

@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, ad__author=request.user)
    ad_id = response.ad.id
    response.delete()
    return redirect('ad_responses', ad_id=ad_id)


@login_required
def create_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ResponseForm()
    return render(request, 'ads/create_response.html', {'form': form, 'ad': ad})

@login_required
def private_page(request):
    ads = Ad.objects.filter(author=request.user)
    selected_ad = request.GET.get('ad')
    if selected_ad:
        responses = ads.get(id=selected_ad).responses.all()
    else:
        responses = []

    return render(request, 'ads/private_page.html', {
        'ads': ads,
        'responses': responses,
    })

def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.status = 'accepted'
    response.save()

    # Отправка уведомления по e-mail
    send_mail(
        'Ваш отклик принят!',
        'Ваш отклик на объявление "{}" был принят.'.format(response.ad.title),
        'from@example.com',
        [response.author.email],
        fail_silently=False,
    )
    return redirect('private_page')

@login_required
def add_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ResponseForm()
    return render(request, 'ads/add_response.html', {'form': form, 'ad': ad})