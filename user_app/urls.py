from django.urls import path
from .views import user_register

app_name = 'user'

urlpatterns = [
    path('register/', user_register, name='register')
]