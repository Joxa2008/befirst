from django.urls import path
from .views import main, profile_update, experts_score, work_detail

app_name = 'contest'
urlpatterns = [
    path('', main, name='main'),
    path('profile/update', profile_update, name='profile_update'),
    path('experts/works-to-check/', experts_score, name='experts_score'),
    path('experts/works-to-check/<str:uuid>', work_detail, name='work_detail')
]