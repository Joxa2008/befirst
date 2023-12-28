from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegistrationCompleteForm, GiveScoreForm, UserProfileUpdateForm
from .models import ProfileModel, ExpertModel, ScoreModel, WorkModel, ContestModel, Region, CommentModel
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
# import user_app
# from user_app.models import CustomUserModel
from datetime import date
import requests
from django.core.paginator import Paginator

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


def contests(request):
    contest = ContestModel.objects.all()
    return render(request, 'contests.html', context={
        'contests': contest
    })


def ditail(request, slug):
    contest = ContestModel.objects.get(slug=slug)
    comments = CommentModel.objects.select_related().filter(comment_receiver=contest)[::-1]
    comments = comments[:4]
    form = PostComment()
    if requests.method == 'POST':
        form = PostComment(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.comment_receiver = contest
            data.comment_owner = ProfileModel.objects.get(user=requests.user)
            data.save()

    return render(request, 'ditail.html', context={
        'contest': contest,
        'comments': comments,
    })


def statistic(request):
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

    return render(request, 'map.html', context={
        'data': data_list
    })


def results(request):
    return render(request, 'resoults.html')


def contactsView(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]

        text = "Customer details: \n"
        text += f"Name: {name}\n"
        text += f"Email: {email}\n"
        text += f"Message from customer: {message}\n"
        token = '6776522922:AAGwx9g2ez2l-0M40r2sJ2npNpH2rV_V0dY'
        id = "957633020"
        url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id='
        requests.get(url + id + '&text=' + text)
        return redirect('contest:contacts')
    return render(request, template_name='contact-page.html', context={})


def anketaView(request):
    year = date.today().year
    profile_m = ProfileModel.user
    print(year)
    user = request.user
    if request.method == 'POST':
        profile = request.user.profile
        print(profile)
        # contest = ContestModel.objects.get("dada")
        comment = request.POST['comment']
        file_u = request.FILES["file"]
        work_m = WorkModel(profile=profile, title=comment, file=file_u)
        work_m.save()
        return redirect('contest:anketa')
    return render(request, template_name='anketa-page.html', context={"user": user, "year": year})


def workView(request):
    works = WorkModel.objects.all()
    paginator = Paginator(works, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # paginator = Paginator()
    if request.method == "POST":
        search = request.POST['search']
        print(search)
        # if search != "":
        works = works.filter(~Q(title__icontains=search))
        searched = WorkModel.objects.filter(title__icontains=search)
        print(searched)
        return render(request, template_name='works-page.html',
                      context={"works": works, "search": search, "searched": searched, "page_obj": page_obj})
    else:
        return render(request, template_name='works-page.html',
                      context={"works": works, "page_obj": page_obj
                               })


