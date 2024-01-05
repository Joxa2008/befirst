from django.contrib import admin
from .models import Region, ContestModel, ExpertModel, ProfileModel, ScoreModel, WorkModel

admin.site.register(Region)
admin.site.register(ScoreModel)


@admin.register(ContestModel)
class ContestAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    filter_horizontal = ['experts']

@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


@admin.register(ExpertModel)
class ExpertAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


@admin.register(WorkModel)
class WorkModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'contest', 'uploaded_at', 'place')
    list_display_links = ('title', 'uploaded_at')
    date_hierarchy = 'uploaded_at'
    list_filter = ('uploaded_at',)
    ordering = ('uploaded_at',)
    fieldsets = [
        ('User Related', {'fields': ['profile', 'contest']}),
        ('Other Data', {'classes': ['collapse'], 'fields': ['title', 'file']})
    ]
