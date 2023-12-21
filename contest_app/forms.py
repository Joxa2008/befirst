from django import forms
from .models import ProfileModel


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['region', 'address', 'news_agreement', 'profile_img']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control pt-2 pt-sm-3',
                'style': 'resize: none; margin-top: 5px; height: min(12vw, 65px);',
            }),
            'news_agreement': forms.CheckboxInput(attrs={
                'class': 'reg-checkbox news-agree-check position-absolute z-2',
                'onclick': "regCheckboxValidate()"
            }),
            'profile_img': forms.FileInput(attrs={
                'class': 'form-control pt-2 pt-sm-3',
                'accept': ".jpg, .jpeg, .png"})
        }
