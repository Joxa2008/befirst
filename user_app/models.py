from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Choices
from contest_app.models import Region


class CustomUserModel(AbstractUser):
    def user_directory_path(instance, filename):
        return 'users/{0}/profile/{1}'.format(instance.username, filename)

    first_name = models.CharField(blank=False, null=False, max_length=150)

    last_name = models.CharField(blank=False, null=False, max_length=150)

    email = models.CharField(blank=False, null=False, unique=True, max_length=100,
                             help_text='Field is unique. You can register with this email only once')
    profile_img = models.ImageField(upload_to=user_directory_path,
                                    blank=True, null=True,
                                    help_text='Your profile picture.')

    phone_number = models.CharField(max_length=13, blank=True, null=True, help_text='Enter phone number.')

    birth_date = models.DateField(blank=False, null=False)

    CHOICES = (('M', 'Male'), ('F', 'Female'))

    gender = models.CharField(blank=False, null=False, max_length=1, choices=CHOICES, default='M')

    password = models.CharField(blank=False, null=False, max_length=100, help_text='Create your own password.')

    news_agreement = models.BooleanField(blank=False, null=False, default=False,
                                         help_text='Are you agree to receive news from BeFirst?')

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True,  related_name='users')

    address = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ['birth_date', 'gender', 'news_agreement']

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
