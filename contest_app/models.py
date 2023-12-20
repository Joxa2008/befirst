from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# from datetime import datetime
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False,
                            help_text=_("Required. The name of the region."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
        db_table = 'region'


class ProfileModel(models.Model):
    def user_directory_path(instance, filename):
        return f'users/{instance.user_id}/profile/{filename}'

    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_("Choose a user."), related_name='profile')

    profile_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True,
                                    help_text=_('Your profile picture. .jpg, .jpeg, .png only!'))

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True,
                               help_text=_("Choose a region you reside. e.g. 'Samarkand'"))
    address = models.TextField(blank=True, null=True,
                               help_text=_("Enter your address here. e.g: 45/9 Sergeli 7, Tashkent Shahar"))
    news_agreement = models.BooleanField(default=True, help_text=_("Do you want to receive e-mails from us? "
                                                                   "e.g: information about new contests"))

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        db_table = 'profile'


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        obj = ProfileModel.objects.create(user=instance)
        obj.save()


class ExpertModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, help_text=_("Choose an expert."),
                                related_name='expert')
    detail = models.TextField(blank=True, null=True, help_text=_("Some details about the expert."))

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'expert'
        verbose_name_plural = 'experts'
        db_table = 'expert'


class ContestModel(models.Model):

    def user_directory_path(instance, filename):
        return "contests/{0}/{1}".format(instance.slug, filename)

    title = models.CharField(max_length=150, help_text=_("Enter a title of the contest."))

    slug = models.SlugField(null=True, blank=True, unique=True,
                            help_text=_(
                                "a slug that appears in the url. If not provided, 'title' will be used instead"))

    description = models.TextField(blank=True, null=True, help_text=_("Description of the contest."))

    banner_image = models.ImageField(upload_to=user_directory_path,
                                     help_text=_("Required. A banner image of the contest"))

    start_date = models.DateTimeField(help_text=_("Required. The start date of the contest."))

    end_date = models.DateTimeField(help_text=_("Required. The end date of the contest."))

    publish_date = models.DateTimeField(help_text=_("Required. The date when results will be published."))

    experts = models.ManyToManyField(ExpertModel, help_text=_("Required. Select experts for the contest."),
                                     related_name="contests")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # UNCOMMENT this when urls.py and template for contest_detail are ready

    # def get_absolute_url(self):
    #     return reverse('contest_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.title)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = ContestModel.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '-' + str(counter)
                        counter += 1
                except ContestModel.DoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super().clean()
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be greater than start date.')
        elif self.publish_date < self.end_date:
            raise ValidationError('Publish date must be greater than or equal to the End date.')

    class Meta:
        verbose_name = 'contest'
        verbose_name_plural = 'contests'
        db_table = 'contest'


class WorkModel(models.Model):
    def user_directory_path(instance, filename):
        return "works/{0}/{1}/{2}".format(instance.profile, instance.contest.slug, filename)

    profile = models.ForeignKey(ProfileModel, on_delete=models.SET_NULL, null=True, related_name='works')

    contest = models.ForeignKey(ContestModel, on_delete=models.SET_NULL, null=True, related_name='works')

    title = models.CharField(max_length=100, help_text=_("Enter the title of a work."))

    file = models.FileField(upload_to=user_directory_path, help_text=_("Upload the file."))

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'work'
        verbose_name_plural = 'works'
        db_table = 'work'


class ScoreModel(models.Model):
    expert = models.ForeignKey(ExpertModel, on_delete=models.SET_NULL, null=True, related_name='scores')

    CHOICES = (
        (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5), (6, 6), (7, 7),
        (8, 8), (9, 9), (10, 10)
    )

    scale = models.PositiveIntegerField(choices=CHOICES, default=1,
                                        help_text=_("How would you assess the work on the scale from 1 to 10?"))

    work = models.ForeignKey(WorkModel, on_delete=models.SET_NULL, null=True, blank=False, related_name='scores')

    def __str__(self):
        return f'{self.work}: {self.scale} by {self.expert}'

    class Meta:
        verbose_name = 'score'
        verbose_name_plural = 'scores'
        db_table = 'score'
