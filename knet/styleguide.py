from django.shortcuts import render

import floppyforms as forms


def styleguide(request):
    form = StyleguideTestForm()
    return render(request, 'styleguide/styleguide.html', {'form': form})


class StyleguideTestForm(forms.Form):
    text = forms.CharField(required=True)
    url = forms.URLField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    date = forms.DateField()
    time = forms.TimeField()
    datetime = forms.DateTimeField()
    number = forms.DecimalField()
    attachment = forms.FileField()
    textarea = forms.CharField(widget=forms.Textarea)
    checkbox = forms.BooleanField()
    select = forms.ChoiceField(
        choices=[
            ('us', 'United States'),
            ('ca', 'Canada'),
            ('mx', 'Mexico')])
    multiple = forms.MultipleChoiceField(
        choices=[
            ('us', 'United States'),
            ('ca', 'Canada'),
            ('mx', 'Mexico')])
    radio = forms.ChoiceField(
        choices=[
            ('us', 'United States'),
            ('ca', 'Canada'),
            ('mx', 'Mexico')],
        widget=forms.RadioSelect)
