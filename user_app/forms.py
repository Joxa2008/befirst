from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


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
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.com', 'class': "form-control"}),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'firstname',
                'class': "form-control"}),

            'birth_date': forms.SelectDateWidget(attrs={
                'class': "form-control"}),

            'gender': forms.Select(attrs={
                'class': "form-control"}),

            'phone_number': forms.TextInput(attrs={
                'class': "form-control"}),

            'password': forms.PasswordInput(attrs={
                'class': "form-control"})

        }

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match!')
        return self.cleaned_data
