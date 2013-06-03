"""Accounts admin."""
from copy import copy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
import floppyforms as forms

from .models import User


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        widgets = {'name': forms.TextInput}


class UserAdmin(BaseUserAdmin):
    fieldsets = copy(BaseUserAdmin.fieldsets)
    fieldsets[1][1]['fields'] = [
        'name', 'bio', 'first_name', 'last_name', 'email']
    list_display = ['username', 'email', 'name', 'is_staff']
    search_fields = ['username', 'name', 'first_name', 'last_name', 'email']

    form = UserChangeForm


admin.site.register(User, UserAdmin)
