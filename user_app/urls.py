from django.urls import path
from .views import user_register_view, logout_view, user_login_view, comfirm_code, password_change, email_enter

app_name = 'user'

urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', user_login_view, name='login'),
    path('email_enter/', email_enter, name='enter_email'),
    path('comfirm_code/<str:email>/', comfirm_code, name='confirm_code'),
    path('password_change/<str:uuid>/', password_change, name='password_change')
]