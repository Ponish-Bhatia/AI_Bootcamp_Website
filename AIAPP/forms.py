from django import forms
from .models import Img

class ImageUploadUSA(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['image']

class TextFormClass(forms.Form):
    proteins = forms.CharField()
    carbohydrates = forms.CharField()
    fats = forms.CharField()
