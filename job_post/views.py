from django.shortcuts import render
from django.db.models import Q

from .models import *
# Create your views here.
def index(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = JobPost.objects.filter(
            Q(job_title__icontains=search_term) |
            Q(job_type__icontains=search_term) |
            Q(job_desc__icontains=search_term) |
            Q(job_requirements__icontains=search_term) |
            Q(job_location__icontains=search_term) |
            Q(job_status__icontains=search_term) 
            )
    else:
        all_job_posts = JobPost.objects.all()    
    return render(request, 'job_post/index.html', {
        'all_job_posts': all_job_posts,
        'search_term': request.GET.get('search_term')
    })