from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
        db_table = 'region'
