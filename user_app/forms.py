from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
User = get_user_model()
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        'class': "form-control"
    }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'birth_date', 'gender', 'phone_number', 'password']

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
                format=('%Y-%m-%d')),

            'gender': forms.Select(attrs={
                'class': "form-control"}),

            'phone_number': forms.TextInput(attrs={
                'class': "form-control"}),

            'password': forms.PasswordInput(attrs={
                'class': "form-control",
                'placeholder': 'password'})

        }

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match!')
        return self.cleaned_data


class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label=_('Email or Mobile'),
                                     widget=forms.TextInput(attrs={
                                         'class': "form-control"
                                     }),
                                     help_text=_("Enter your email or phone number"), required=True)

    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': _('your password'),
                                   'class': "form-control"
                               }),
                               help_text=_("Enter your password"), required=True)