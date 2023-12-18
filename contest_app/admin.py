from django.contrib import admin
from .models import Region, ContestModel, ExpertModel, ProfileModel, ScoreModel, WorkModel

admin.site.register(Region)
admin.site.register(ExpertModel)
admin.site.register(ProfileModel)
admin.site.register(ScoreModel)
admin.site.register(WorkModel)


@admin.register(ContestModel)
class ContestAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
