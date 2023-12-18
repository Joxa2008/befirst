from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from contest_app.forms import ProfileUpdateForm
from contest_app.views import ProfileModel
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUserModel


def user_register(request):
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


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('contest:main')
