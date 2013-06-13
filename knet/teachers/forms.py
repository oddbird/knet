import floppyforms as forms

from .models import Story, TeacherProfile



class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['body', 'private']
        widgets = {
            'body': forms.Textarea,
            'private': forms.CheckboxInput,
            }


    def __init__(self, user, profile, *args, **kw):
        """
        Accept ``user`` and ``profile`` arguments in addition to normal args.

        ``user`` should be the ``User`` leaving a story.

        ``profile`` should be the ``TeacherProfile`` for whom the story is
        being left.

        """
        self.user = user
        self.profile = profile
        super(StoryForm, self).__init__(*args, **kw)
        self.fields['body'].error_messages['required'] = (
            "You seem to have left your story blank.")


    def save(self, commit=True):
        """Save the story for the given profile from given user."""
        story = super(StoryForm, self).save(commit=False)
        story.profile = self.profile
        story.submitter = self.user
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
