from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password
from contest_app.forms import ProfileUpdateForm
from contest_app.views import ProfileModel
from django.contrib.auth import authenticate, login
from .models import CustomUserModel, CodeCheck
from django.core.mail import send_mail
from django.conf import settings
import random
import uuid as ui


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

                return render(request, template_name='profile_register.html', context={
                    'form': profile_form
                })
        return render(request, template_name='user_register.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('contest:main')


def email_enter(request):
    message = ''
    if request.method == 'POST':
        mail = request.POST['email']
        try:
            CustomUserModel.objects.get(email=mail)
            status = True
        except:
            message = 'Invalid email'
            status = False

        if status == True:
            integer = random.randint(100000, 999999)
            CodeCheck.objects.create(email=mail, code=integer)

            send_mail(
                'Hello',
                f'{integer}',
                'settings.EMAIL_HOST_USER',
                [mail],
                fail_silently=False
            )

            return redirect('user:confirm_code', email=mail)

    return render(request, 'enter_email.html', context={
        'message': message
    })


def comfirm_code(request, email):
    message = ''
    if request.method == 'POST':
        z = ''.join([request.POST[f'inp{i}'] for i in range(1, 7)])
        code = CodeCheck.objects.filter(email=email).last()
        print(code)
        if int(code.code) == int(z):
            uid = CustomUserModel.objects.get(email=email)
            CodeCheck.objects.filter(email=email).delete()
            return redirect('user:password_change', uuid=uid.uuid)
        else:
            message = 'Invalid code'

    return render(request, 'comfirm_code.html', context={
        'message': message
    })


def password_change(request, uuid):
    if request.method == 'POST':
        new_p = request.POST['password']
        user = CustomUserModel.objects.get(uuid=uuid)
        user.password = make_password(new_p)
        user.uuid = ui.uuid4()
        user.save()
    return render(request, 'forget_p.html')
