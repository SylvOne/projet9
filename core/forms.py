from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CritiqueForm(forms.Form):
    image_upload = forms.ImageField(required=True)
    title = forms.CharField(max_length=100, required=True)
    caption = forms.CharField(widget=forms.Textarea, required=True)
    title_review = forms.CharField(max_length=100, required=True)
    radio = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        required=True
    )
    commentaire = forms.CharField(widget=forms.Textarea, required=True)

class RequestCritiqueForm(forms.Form):
    image_upload = forms.ImageField(required=True)
    title = forms.CharField(max_length=100, required=True)
    caption = forms.CharField(widget=forms.Textarea, required=True)