from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse

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
    })
    
def companies(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_companies = Company.objects.filter(
            Q(comp_name__icontains=search_term) |
            Q(comp_desc__icontains=search_term) 
            )
    else:
        all_companies = Company.objects.all()    
    return render(request, 'job_post/companies.html', {
        'all_companies': all_companies,
    })
    
def create_company(request):
    if request.method == "POST":
        return HttpResponse(request)
    
    return render(request, 'job_post/create_company.html', {
        
    })
    
def favourite(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = request.user.favourite_posts.filter(
            Q(job_title__icontains=search_term) |
            Q(job_type__icontains=search_term) |
            Q(job_desc__icontains=search_term) |
            Q(job_requirements__icontains=search_term) |
            Q(job_location__icontains=search_term) |
            Q(job_status__icontains=search_term) 
            )
    else:
        all_job_posts = request.user.favourite_posts.all()    
    return render(request, 'job_post/favourite.html', {
        'all_job_posts': all_job_posts,
    })
    
def following(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = JobPost.objects.filter(company__in=request.user.followed_company.all()).filter(
            Q(job_title__icontains=search_term) |
            Q(job_type__icontains=search_term) |
            Q(job_desc__icontains=search_term) |
            Q(job_requirements__icontains=search_term) |
            Q(job_location__icontains=search_term) |
            Q(job_status__icontains=search_term) 
            )
    else:
        all_job_posts = JobPost.objects.filter(company__in=request.user.followed_company.all())
    return render(request, 'job_post/following.html', {
        'all_job_posts': all_job_posts,
        'followed_companies': request.user.followed_company.all()
    })
    
def followed_companies(request):
    return HttpResponse('followed_companies')