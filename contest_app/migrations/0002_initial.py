# Generated by Django 5.0 on 2023-12-15 14:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='expertmodel',
            name='user',
            field=models.OneToOneField(help_text='Choose the expert.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expert', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contestmodel',
            name='experts',
            field=models.ManyToManyField(help_text='Select the experts of the contest.', related_name='contests', to='contest_app.expertmodel'),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='user',
            field=models.OneToOneField(help_text='Choose the user.', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='region',
            field=models.ForeignKey(help_text="Choose the region you reside. e.g. 'Samarkand'", on_delete=django.db.models.deletion.CASCADE, to='contest_app.region'),
        ),
        migrations.AddField(
            model_name='scoremodel',
            name='expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scores', to='contest_app.expertmodel'),
        ),
        migrations.AddField(
            model_name='workmodel',
            name='contest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='works', to='contest_app.contestmodel'),
        ),
        migrations.AddField(
            model_name='workmodel',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='works', to='contest_app.profilemodel'),
        ),
        migrations.AddField(
            model_name='scoremodel',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scores', to='contest_app.workmodel'),
        ),
    ]
