from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ProfileModel, ContestModel
from celery import current_app
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from contest_app.tasks import bar
import json

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        obj = ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=ContestModel)
def pre_save_contest_signal(sender, instance, created, **kwargs):
    if created:
        formatted_datetime = str(instance.publish_date)[0:19]

        # Create a new ClockedSchedule for the specific date and time
        clocked_schedule = ClockedSchedule.objects.create(
            clocked_time=formatted_datetime,
        )

        # Create a new periodic task and associate it with the ClockedSchedule
        task = PeriodicTask.objects.create(
            name=f'{instance.slug}',
            task='contest_app.tasks.bar',  # Replace with your actual task path
            clocked=clocked_schedule,
            one_off=True,
            args=["lolypop", "john_wiek"]
        )

        # Enable the task
        task.enabled = True
        task.save()
        instance.save()

    if not created:
        print(instance.slug)
        task = PeriodicTask.objects.get(name=f'{instance.slug}')
        task.delete()

        formatted_datetime = str(instance.publish_date)[0:19]

        # Create a new ClockedSchedule for the specific date and time
        clocked_schedule = ClockedSchedule.objects.create(
            clocked_time=formatted_datetime,
        )

        args = json.dumps([f"{instance.slug}"])

        task = PeriodicTask.objects.create(
            name=f'{instance.slug}',
            task='contest_app.tasks.bar',  # Replace with your actual task path
            clocked=clocked_schedule,
            one_off=True,
            args=args
        )

        task.save()
