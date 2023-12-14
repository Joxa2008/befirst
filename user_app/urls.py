from django.urls import path

from contest_app.views import main
urlpatterns = [
    path('user/', main, name='main1')
]