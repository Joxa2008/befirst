from django.urls import path
from .views import main_view, register_complete_view, experts_score_view, work_detail_view, \
    user_update_view, contests, ditail, statistic, results, contactsView, anketaView, workView

app_name = 'contest'
urlpatterns = [
    path('', main_view, name='main'),
    path('register/complete/', register_complete_view, name='register_complete'),
    path('experts/works-to-check/', experts_score_view, name='experts_score'),
    path('experts/works-to-check/<str:uuid>', work_detail_view, name='work_detail'),
    path('profile/update/', user_update_view, name='user_update'),
    path('contests/', contests, name='contests'),
    path('ditail/<str:slug>/', ditail, name='contest-ditail'),
    path('statistic/', statistic, name='static'),
    path('results_data/', results, name='results'),
    path('contacts/', contactsView, name='contacts'),
    path('contests/anketa/', anketaView, name='anketa'),
    path('contests/work/', workView, name='work'),
]
