"""Accounts admin."""
from copy import copy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import forms as authforms
import floppyforms as forms

from .models import User


class UserChangeForm(authforms.UserChangeForm):
    class Meta:
        model = User
        widgets = {'name': forms.TextInput}


class UserCreationForm(authforms.UserCreationForm):
    class Meta:
        model = User


    def clean_username(self):
        # The superclass version of this hardcodes auth.User model.
        # We don't need the nicer error, default ORM unique validation is fine.
        return self.cleaned_data["username"]


class UserAdmin(BaseUserAdmin):
    fieldsets = copy(BaseUserAdmin.fieldsets)
    fieldsets[1][1]['fields'] = [
        'name', 'bio', 'first_name', 'last_name', 'email']
    list_display = ['username', 'email', 'name', 'is_staff']
    search_fields = ['username', 'name', 'first_name', 'last_name', 'email']

    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
