from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'email', 'email_confirmed', 'is_staff', 'delete_link']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('delete_user/<int:user_id>/', self.admin_site.admin_view(self.delete_user_view), name='delete_user'),
        ]
        return custom_urls + urls

    def delete_user_view(self, request, user_id):
        return redirect('delete_user', user_id=user_id)

    def delete_link(self, obj):
        return format_html('<a href="{}">Delete</a>', reverse('admin:delete_user', args=[obj.id]))

    delete_link.short_description = 'Delete User'

admin.site.register(CustomUser, CustomUserAdmin)
