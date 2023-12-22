from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .forms import ProfileUpdateForm, GiveScoreForm
from .models import ProfileModel, ExpertModel, ScoreModel, WorkModel
from django.contrib import messages
from django.views.generic import View


def main(request):
    return render(request, 'main.html')


@login_required
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
    messages.success(request, 'Ooops!')
    print('did not get posted!!!')
    return redirect('contest:main')


@login_required
def experts_score(request):
    try:
        expert = request.user.expert
        obj = ExpertModel.objects.prefetch_related('contests__works__scores__expert__user').get(id=expert.id)
        return render(request, 'experts_score.html', {'expert': obj})
    except ExpertModel.DoesNotExist:
        return redirect('contest:main')


def work_detail(request, uuid):
    expert = request.user.expert
    work = WorkModel.objects.get(uuid=uuid)
    if request.method == 'POST':
        form = GiveScoreForm(request.POST)
        if form.is_valid():
            if ScoreModel.objects.filter(expert=request.user.expert, work=work).exists():
                form.add_error('scale', "Expert is already assigned to this work.")
                return render(request, 'work_detail.html', context={
                    'work': work,
                    'form': form})

            score = ScoreModel.objects.create(expert=request.user.expert,
                                              work=work,
                                              scale=form.cleaned_data['scale'])
            print('success')
            obj = ExpertModel.objects.get(id=expert.id)
            return render(request, 'experts_score.html', {'expert': obj})
        print('invalid form')
        return render(request, 'work_detail.html', context={
            'work': work,
            'form': form})

    if request.method == 'GET':
        form = GiveScoreForm()
        return render(request, 'work_detail.html', context={
            'form': form,
            'work': work,
        })
