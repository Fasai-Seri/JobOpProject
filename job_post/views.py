from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.forms import forms
import datetime

from .models import *
# Create your views here.
    
def index(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = JobPost.objects.filter(
            Q(job_title__icontains=search_term) |
            Q(job_type__icontains=search_term) |
            Q(job_desc_text__icontains=search_term) |
            Q(job_requirement_text__icontains=search_term) |
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
            Q(job_desc_text__icontains=search_term) |
            Q(job_requirement_text__icontains=search_term) |
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
            Q(job_desc_text__icontains=search_term) |
            Q(job_requirement_text__icontains=search_term) |
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
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_companies = request.user.followed_company.all().filter(
            Q(comp_name__icontains=search_term) |
            Q(comp_desc__icontains=search_term) 
            )
    else:
        all_companies = request.user.followed_company.all()
    return render(request, 'job_post/followed_companies.html', {
        'all_companies': all_companies
    })
    
def create_job_post(request):
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        job_type = request.POST.get('job_type')
        company = Company.objects.get(pk=request.POST.get('company'))
        job_desc_text = request.POST.get('job_desc_text')
        job_desc_file = request.POST.get('job_desc_file')
        job_requirement_text = request.POST.get('job_requirement_text')
        job_requirement_file = request.POST.get('job_requirement_file')
        job_major = Major.objects.filter(pk__in=request.POST.getlist('job_major'))
        job_post_date = datetime.datetime.now()
        job_close_date =  request.POST.get('job_close_date')
        job_location =  request.POST.get('job_location')
        job_status = 'active'
        new_job_post = JobPost(job_title=job_title, 
                               job_type=job_type, 
                               company=company, 
                               job_desc_text=job_desc_text, 
                               job_desc_file=job_desc_file, 
                               job_requirement_text=job_requirement_text, 
                               job_requirement_file=job_requirement_file,
                               job_post_date = job_post_date,
                               job_close_date = job_close_date,
                               job_location = job_location,
                               job_status = job_status
                               )
        if Employer.objects.filter(user_id=request.user):
            poster_emp = Employer.objects.filter(user_id=request.user).first()
            new_job_post.poster_emp = poster_emp
        elif Professor.objects.filter(user_id=request.user):
            poster_prof = Professor.objects.filter(user_id=request.user).first()
            new_job_post.poster_prof = poster_prof
        new_job_post.save()
        JobPost.objects.last().job_major.set(job_major)
        
        return HttpResponse(job_major)
    
    return render(request, 'job_post/create_job_post.html', {
        'job_type_choices': JobPost.job_type_choices,
        'all_companies': Company.objects.all(),
        'all_major': Major.objects.all()
    })