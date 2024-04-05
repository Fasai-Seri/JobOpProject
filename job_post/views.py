from django.shortcuts import render

from .models import *
# Create your views here.
def index(request):
    return render(request, 'job_opportunity/index.html', {
        'all_job_posts': JobPost.objects.all()
    })