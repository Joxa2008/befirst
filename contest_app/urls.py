from django.urls import path
from .views import main, profile_update, contests, ditail, statistic

app_name = 'contest'
urlpatterns = [
    path('', main, name='main'),
    path('profile/update', profile_update, name='profile_update'),
    path('contests/', contests, name='contests'),
    path('ditail/<str:slug>/', ditail, name='contest-ditail'),
    path('statistic/', statistic, name='static')
]