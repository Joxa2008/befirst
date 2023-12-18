from django.contrib import admin
from .models import Region, ContestModel, ExpertModel, ProfileModel, ScoreModel, WorkModel, CommentModel

admin.site.register(Region)
admin.site.register(ContestModel)
admin.site.register(ExpertModel)
admin.site.register(ProfileModel)
admin.site.register(ScoreModel)
admin.site.register(WorkModel)
admin.site.register(CommentModel)

