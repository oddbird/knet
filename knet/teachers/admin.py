from django.contrib import admin
import floppyforms as forms

from . import models


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = models.TeacherProfile
        widgets = {'school': forms.TextInput}


class TeacherProfileAdmin(admin.ModelAdmin):
    form = TeacherProfileForm


class StoryForm(forms.ModelForm):
    class Meta:
        model = models.Story
        widgets = {'submitter_name': forms.TextInput}


class StoryAdmin(admin.ModelAdmin):
    form = StoryForm


admin.site.register(models.TeacherProfile, TeacherProfileAdmin)
admin.site.register(models.Story, StoryAdmin)