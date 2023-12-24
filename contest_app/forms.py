from django.utils import timezone

from django import forms
from .models import ProfileModel, ScoreModel, Region
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationCompleteForm(forms.ModelForm):
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


class GiveScoreForm(forms.ModelForm):
    class Meta:
        model = ScoreModel
        fields = ['scale']

        widgets = {
            'scale': forms.Select(attrs={'class': 'form-control'})
        }


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'birth_date', 'gender')

class UserProfileUpdateForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[])
    address = forms.CharField(max_length=255, required=False)
    news_agreement = forms.BooleanField(required=False)
    profile_img = forms.FileField(required=False,
                                  widget=forms.FileInput(attrs={'accept': '.jpg, .jpeg, .png',
                                                                'id': 'imageInput', 'onchange': 'displayImage()',
                                                                'title': 'Change Profile Image'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birth_date', 'gender', 'phone_number')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': "form-control"}),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'first name',
                'class': "form-control"}),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'last name',
                'class': "form-control"}),

            'birth_date': forms.DateTimeInput(attrs={
                'class': "form-control",
                'placeholder': 'Select a date',
                'type': 'date',
                'min': f'{timezone.now().year - 18}-{timezone.now().month}-{timezone.now().day}',
                'max': f'{timezone.now().year}-{timezone.now().month}-{timezone.now().day}'},
                format='%Y-%m-%d'),

            'gender': forms.Select(attrs={
                'class': "form-select"}),

            'phone_number': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': '+998 XX XXX XX XX'}),

        }

    # setting initial value for field
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['region'].choices = [(region.name, region.name) for region in Region.objects.all()]

    def save(self, commit=True):
        user_instance = super(UserProfileUpdateForm, self).save(commit=False)
        user_instance.profile.region = Region.objects.get(name=self.cleaned_data.get('region'))
        user_instance.profile.address = self.cleaned_data.get('address')
        user_instance.profile.profile_img = self.cleaned_data.get('profile_img')
        user_instance.profile.news_agreement = self.cleaned_data.get('news_agreement')

        if commit:
            user_instance.save()
            user_instance.profile.save()
        return user_instance
