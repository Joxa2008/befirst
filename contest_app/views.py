from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegistrationCompleteForm, GiveScoreForm, UserProfileUpdateForm
from .models import ProfileModel, ExpertModel, ScoreModel, WorkModel, ContestModel, Region
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def main_view(request):
    return render(request, 'main.html')


@login_required
def register_complete_view(request):
    if request.method == 'POST':
        obj = ProfileModel.objects.get(user=request.user)
        form = RegistrationCompleteForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully completed your profile!')
            return redirect('contest:main')
        messages.success(request, 'Form is invalid!')
        return redirect('contest:main')
    messages.error(request, 'Ooops!')
    return redirect('contest:main')


@login_required
def experts_score_view(request):
    try:
        expert = ExpertModel.objects.prefetch_related('contests__works__scores__expert__user') \
            .get(id=request.user.expert.id)
        return render(request, 'experts_score.html', {'expert': expert})
    except ExpertModel.DoesNotExist:
        return redirect('contest:main')


@login_required
def work_detail_view(request, uuid):
    expert = request.user.expert
    work = WorkModel.objects.get(uuid=uuid)
    if request.method == 'POST':
        form = GiveScoreForm(request.POST)
        if form.is_valid():
            if ScoreModel.objects.filter(expert=request.user.expert, work=work).exists():
                form.add_error('scale', "Expert is already assigned to this work.")
                messages.error(request, 'Expert is already assigned to this work.')
                return render(request, 'work_detail.html', context={
                    'work': work,
                    'form': form})

            score = ScoreModel.objects.create(expert=request.user.expert,
                                              work=work,
                                              scale=form.cleaned_data['scale'])
            return redirect('contest:experts_score')

        return render(request, 'work_detail.html', context={
            'work': work,
            'form': form})

    if request.method == 'GET':
        if work.contest.publish_date <= timezone.now():
            return redirect('contest:experts_score')
        form = GiveScoreForm()
        return render(request, 'work_detail.html', context={
            'form': form,
            'work': work,
        })


@login_required
def user_update_view(request):
    user_instance = User.objects.get(id=request.user.id)
    initial_data = {
        'region': user_instance.profile.region,
        'address': user_instance.profile.address,
        'news_agreement': user_instance.profile.news_agreement,
        'profile_img': user_instance.profile.profile_img,
    }

    user_form = UserProfileUpdateForm(instance=user_instance, initial=initial_data)

    if request.method == 'POST':
        form1 = UserProfileUpdateForm(request.POST, request.FILES, instance=user_instance)
        if form1.is_valid():
            if not form1.cleaned_data['profile_img']:
                form1.cleaned_data['profile_img'] = initial_data['profile_img']
                form1.save()
            form1.save()
            messages.success(request, 'Successfully updated')
            return redirect('contest:user_update')

        if not form1.cleaned_data['profile_img']:
            form1.cleaned_data['profile_img'] = initial_data['profile_img']
        print(form1.cleaned_data)
        return render(request, 'profile_user_update.html', context={
            'form': form1,
        })
    return render(request, 'profile_user_update.html', context={
        'form': user_form,
    })

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

