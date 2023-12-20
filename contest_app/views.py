from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, PostComment
from .models import ProfileModel, ContestModel, CommentModel, Region


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
            return redirect('contest:main')
        logout(request.user)
        print('did no get valid!!!')
        return redirect('contest:main')
    print('did not get posted!!!')
    logout(request.user)
    return redirect('contest:main')


def contests(requests):
    contest = ContestModel.objects.all()
    return render(requests, 'contests.html', context={
        'contests': contest
    })


def ditail(requests, slug):
    contest = ContestModel.objects.get(slug=slug)
    comments = CommentModel.objects.select_related().filter(comment_receiver=contest)[::-1]
    comments = comments[:4]
    form = PostComment()
    if requests.method == 'POST':
        form = PostComment(requests.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.comment_receiver = contest
            data.comment_owner = ProfileModel.objects.get(user=requests.user)
            data.save()

    return render(requests, 'ditail.html', context={
        'contest': contest,
        'comments': comments,
    })


def statistic(requests):
    regions = Region.objects.all()
    data = ProfileModel.objects.all()
    data_list = []
    for i in regions:
        v = 0
        for j in data:
            if j.region == i:
                v += 1
        t = {
            'region': i.name,
            'users': v
        }
        data_list.append(t)

    # Filter qilishim mumkun lekin queery kopayib ketadi

    return render(requests, 'map.html', context={
        'data': data_list
    })


def results(requests):
    return render(requests, 'resoults.html')
