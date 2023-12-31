from django.urls import path
from .views import main_view

app_name = 'aboutUs'
urlpatterns = [
    path('', main_view, name='aboutUs'),
]