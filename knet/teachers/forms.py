import floppyforms as forms

from .models import Story



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


    def save(self, commit=True):
        """Save the story for the appropriate teacher."""
        story = super(StoryForm, self).save(commit=False)
        story.profile = self.profile
        if commit:
            story.save()
        return story
