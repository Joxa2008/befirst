from django.urls import path
from .views import user_register_view, logout_view, user_login_view

app_name = 'user'

urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', user_login_view, name='login')
]