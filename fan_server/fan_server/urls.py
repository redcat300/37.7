from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import register, confirm_email, delete_user
from ads.views import (
    create_ad, delete_ad, ad_detail, category_list, category_ads, add_comment,
    edit_comment, delete_comment, toggle_like, user_ads, ad_responses,
    accept_response, delete_response, private_page, add_response
)
from newsletter.views import subscribe, send_newsletter, subscription_success, unsubscribe, unsubscription_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('confirm/<int:user_id>/', confirm_email, name='confirm_email'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('subscription_success/', subscription_success, name='subscription_success'),
    path('unsubscription_success/', unsubscription_success, name='unsubscription_success'),
    path('ads/create/', create_ad, name='create_ad'),
    path('ads/<int:ad_id>/', ad_detail, name='ad_detail'),
    path('ads/<int:ad_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('ads/<int:ad_id>/like/', toggle_like, name='toggle_like'),
    path('ads/delete/<int:ad_id>/', delete_ad, name='delete_ad'),
    path('newsletter/subscribe/<slug:category>/', subscribe, name='subscribe'),
    path('newsletter/unsubscribe/<slug:category>/', unsubscribe, name='unsubscribe'),
    path('newsletter/send/', send_newsletter, name='send_newsletter'),
    path('categories/', category_list, name='category_list'),
    path('categories/<slug:category>/', category_ads, name='category_ads'),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='home'),
    path('my_ads/', user_ads, name='user_ads'),
    path('ad/<int:ad_id>/responses/', ad_responses, name='ad_responses'),
    path('private/', private_page, name='private_page'),  # Маршрут для приватной страницы
    path('response/<int:response_id>/accept/', accept_response, name='accept_response'),
    path('response/<int:response_id>/delete/', delete_response, name='delete_response'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ads/<int:ad_id>/respond/', add_response, name='add_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
