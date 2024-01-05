from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from user_app.models import CustomUserModel
from .models import ContestModel, WorkModel, ScoreModel, ProfileModel


@shared_task
def bar(arg1):
    contest = ContestModel.objects.get(slug=arg1)
    work = WorkModel.objects.filter(contest=contest)
    if len(work) > 3:
        l = []
        for works in work:
            one = ScoreModel.objects.filter(work=works)
            if len(one) == 0:
                pass
            else:
                scales = [int(i.scale) for i in one]
                if len(scales) < 4:
                    for i in range(len(scales), 5):
                        scales.append(sum(scales) / len(scales))

            l.append((works.id, sum(scales)))

        l = sorted(l, key=lambda x: x[1])

        for i in range(len(l)):
            winner = CustomUserModel.objects.get(email=WorkModel.objects.get(id=l[i][0]).profile.user.email)
            works = WorkModel.objects.get(id=int(l[i][0]))
            works.place = i+1
            works.save()
            title = f'Hello {winner.first_name} {winner.last_name}'
            if i == 0:
                text = f'Congratulations you win {contest.title} competition!'
            elif i == 1:
                text = f'Congratulations you get second place in {contest.title} competition!'
            elif i == 2:
                text = f'Congratulations you get third place in {contest.title} competition!'

            if i in range(0, 3):
                send_mail(
                    f'{title}',
                    f'{text}',
                    'settings.EMAIL_HOST_USER',
                    [f'{winner.email}'],
                    fail_silently=False
                )


    else:
        return 'Competition canceled'

    return 'good'
