# Generated by Django 5.0 on 2023-12-18 15:21

import user_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_alter_customusermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='phone_number',
            field=models.CharField(blank=True, error_messages={'invalid': 'Please enter a valid phone', 'unique': 'A user with that phone number already exists'}, help_text='Enter phone number e.g: +998123456789', max_length=13, null=True, unique=True, validators=[user_app.validators.PhoneValidator], verbose_name='phone number'),
        ),
    ]
