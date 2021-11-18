from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class UsersAdmin(UserAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'is_active']
    list_display_links = ['first_name', 'last_name', 'username']
    search_fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_active',
                     'is_superuser', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_superuser', 'is_staff', 'date_joined']


admin.site.register(CustomUser, UsersAdmin)
