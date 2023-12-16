from django.contrib.auth import authenticate
from django.shortcuts import render
from .forms import RegisterForm
from contest_app.forms import ProfileUpdateForm
from contest_app.views import ProfileModel
from django.contrib.auth import authenticate, login


def user_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            del form.cleaned_data['confirm_password']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()

            profile_form = ProfileUpdateForm(instance=ProfileModel.objects.get(user=user))

            auth_user = authenticate(email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)

            return render(request, template_name='profile_register.html', context={
                'form': profile_form
            })
    return render(request, template_name='user_register.html', context={'form': form})
