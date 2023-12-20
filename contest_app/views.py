from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from .models import ProfileModel
from django.contrib import messages


def main(request):
    return render(request, 'main.html')


def profile_update(request):
    if request.method == 'POST':
        print('got posted!!!')
        obj = ProfileModel.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            print('got valid!!!')
            form.save()
            print('got saved!!!')
            messages.success(request, 'You successfully completed your profile!')
            return redirect('contest:main')
        print('did no get valid!!!')
        messages.success(request, 'Form is invalid!')
        return redirect('contest:main')
    messages.success(request, 'Form is invalid!')
    print('did not get posted!!!')
    return redirect('contest:main')
