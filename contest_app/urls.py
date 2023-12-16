from django.urls import path
from .views import main, profile_update

app_name = 'contest'
urlpatterns = [
    path('', main, name='main'),
    path('profile/update', profile_update, name='profile_update')
]