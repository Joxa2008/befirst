from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from .models import ProfileModel


def main(request):
    return render(request, 'main.html')


def profile_update(request):
    if request.method == 'POST':
        print('got posted!!!')
        obj = ProfileModel.objects.get(user=request.user)
        print(type(obj))
        form = ProfileUpdateForm(request.POST, instance=obj)
        print(form.errors)
        if form.is_valid():
            print('got valid!!!')
            form.save()
            print('got saved!!!')
            return redirect('contest:main')
        logout(request.user)
        print('did no get valid!!!')
        return redirect('contest:main')
    print('did not get posted!!!')
    logout(request.user)
    return redirect('contest:main')

