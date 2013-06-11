import floppyforms as forms

from .models import Story, TeacherProfile



class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['body', 'private', 'submitter_name', 'submitter_email']
        widgets = {
            'body': forms.Textarea,
            'private': forms.CheckboxInput,
            'submitter_name': forms.TextInput,
            'submitter_email': forms.EmailInput,
            }


    def __init__(self, profile, *args, **kw):
        """
        Accept ``profile`` argument in addition to normal ``ModelForm`` args.

        ``profile`` should be a ``TeacherProfile`` instance.

        """
        self.profile = profile
        super(StoryForm, self).__init__(*args, **kw)
        self.fields['body'].error_messages['required'] = (
            "You seem to have left your story blank.")
        self.fields['submitter_email'].error_messages['invalid'] = (
            "That doesn't look like an email address; double-check it?")


    def save(self, commit=True):
        """Save the story for the appropriate teacher."""
        story = super(StoryForm, self).save(commit=False)
        story.profile = self.profile
        if commit:
            story.save()
        return story



class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        widgets = {
            'school': forms.TextInput,
            'bio': forms.Textarea,
            }
        fields = ['school', 'bio']


    def __init__(self, user, *args, **kw):
        """Accept ``user`` argument in addition to normal ``ModelForm`` args."""
        self.user = user
        super(TeacherProfileForm, self).__init__(*args, **kw)


    def save(self, commit=True):
        """Save the profile for the appropriate user."""
        profile = super(TeacherProfileForm, self).save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile
