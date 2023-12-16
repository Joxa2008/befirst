from django.urls import path
from .views import user_register, logout_view

app_name = 'user'

urlpatterns = [
    path('register/', user_register, name='register'),
    path('logout/', logout_view, name='logout')
]