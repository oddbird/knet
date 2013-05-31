from django.contrib import admin
import floppyforms as forms

from .models import TeacherProfile


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        widgets = {'school': forms.TextInput}


class TeacherProfileAdmin(admin.ModelAdmin):
    form = TeacherProfileForm


admin.site.register(TeacherProfile, TeacherProfileAdmin)
