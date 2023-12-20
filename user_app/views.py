from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import CustomUserModel
from contest_app.forms import ProfileUpdateForm
from contest_app.views import ProfileModel
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re
import phonenumbers


def user_register_view(request):
    if request.user.is_authenticated:
        return redirect('contest:main')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                del form.cleaned_data['confirm_password']
                if len(form.cleaned_data['password']) < 5:
                    form.add_error('password', 'Password must be at least 5')
                    return render(request, template_name='user_register.html', context={'form': form})
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                form.save()

                profile_form = ProfileUpdateForm(instance=ProfileModel.objects.get(user=user))

                auth_user = authenticate(email=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'])
                if auth_user is not None:
                    login(request, auth_user)
                messages.success(request, 'You are successfully registered!')
                return render(request, template_name='profile_register.html', context={
                    'form': profile_form
                })
        return render(request, template_name='user_register.html', context={'form': form})


def user_login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            email_or_phone = form.cleaned_data['email_or_phone']

            def validate(value):
                if len(value) != 13 or not value.startswith("+998"):
                    return False
                try:
                    z = phonenumbers.parse(value)  # 998944009080
                    if not phonenumbers.is_valid_number(z):
                        return False
                    return True
                except:
                    return False

            pattern = r"[\w-]{1,20}@gmail\.com"
            if re.match(pattern, email_or_phone):
                user = authenticate(email=email_or_phone, password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You have successfully logged In!')
                    return redirect('contest:main')
                else:
                    form.add_error('password', "Email or password was incorrect")
                    # messages.error(request, 'Email or password was incorrect')
                    return render(request, template_name='login.html', context={'email_or_phone': email_or_phone,
                                                                                'form': form})
            elif validate(email_or_phone):
                try:
                    obj = CustomUserModel.objects.get(phone_number=email_or_phone)
                except CustomUserModel.DoesNotExist:
                    form.add_error('password', "No user for this phone number")
                    # messages.error(request, 'No user for this phone number')
                    return render(request, template_name='login.html', context={'email_or_phone': email_or_phone,
                                                                                'form': form})
                else:
                    user = authenticate(email=obj.email, password=form.cleaned_data['password'])
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'You have successfully logged In!')
                        return redirect('contest:main')
                    else:
                        form.add_error('password', "Password was incorrect")
                        # messages.error(request, 'Password was incorrect')
                        return render(request, template_name='login.html', context={'email_or_phone': email_or_phone,
                                                                                    'form': form})

            else:
                form.add_error('password', "Invalid email or phone number")
                # messages.error(request, 'Phone | Email number or password was incorrect')
                return render(request, template_name='login.html', context={'email_or_phone': email_or_phone,
                                                                            'form': form})

    return render(request, 'login.html', context={'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You logged out!')
    return redirect('contest:main')
