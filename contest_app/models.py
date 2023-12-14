from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
        db_table = 'region'
