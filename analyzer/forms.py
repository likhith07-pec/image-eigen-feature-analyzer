from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=False)
    k = forms.IntegerField(min_value=1, required=False, initial=8)
    image_name = forms.CharField(required=False, widget=forms.HiddenInput)
