from django.shortcuts import render
from contest_app.models import ExpertModel, WorkModel


def main_view(request):
    experts = ExpertModel.objects.prefetch_related('contests__works__scores__expert__user')[:16]
    works = WorkModel.objects.all()

    return render(request, 'about_us.html', context={
        "experts": {experts[0].profile_img},
        "works": works
         
        })
