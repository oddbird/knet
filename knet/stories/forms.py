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


    def __init__(self, *args, **kw):
        self.teacher = args[0]
        super(StoryForm, self).__init__(*args[1:], **kw)
        self.fields['body'].label = "Leave a story for {}".format(self.teacher)
        self.fields['private'].label = "Keep this story private"
        self.fields['submitter_name'].label = "Name"
        self.fields['submitter_email'].label = "Email"


    def save(self, commit=True):
        """Save the story for the appropriate teacher."""
        story = super(StoryForm, self).save(commit=False)
        story.teacher = self.teacher
        if commit:
            story.save()
        return story
