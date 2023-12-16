from django import forms
from .models import ProfileModel


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['region', 'address', 'news_agreement', 'profile_img']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'news_agreement': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'profile_img': forms.FileInput(attrs={'class': 'form-control'})
        }