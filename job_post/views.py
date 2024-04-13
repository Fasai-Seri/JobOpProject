from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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
            Q(job_status__icontains=search_term) |
            Q(company__comp_name__icontains=search_term) |
            Q(company__comp_desc__icontains=search_term) 
            )
    else:
        all_job_posts = JobPost.objects.all()    
    return render(request, 'job_post/index.html', {
        'all_job_posts': all_job_posts,
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
            Q(job_status__icontains=search_term) |
            Q(company__comp_name__icontains=search_term) |
            Q(company__comp_desc__icontains=search_term) 
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
            Q(job_status__icontains=search_term) |
            Q(company__comp_name__icontains=search_term) |
            Q(company__comp_desc__icontains=search_term) 
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
        job_requirement_text = request.POST.get('job_requirement_text')
        job_major = Major.objects.filter(pk__in=request.POST.getlist('job_major'))
        job_post_date = datetime.datetime.now()
        job_close_date =  request.POST.get('job_close_date')
        job_location =  request.POST.get('job_location')
        job_status = 'active'
        new_job_post = JobPost(job_title=job_title, 
                               job_type=job_type, 
                               company=company, 
                               job_desc_text=job_desc_text, 
                               job_requirement_text=job_requirement_text, 
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
        
        saved_job_post = JobPost.objects.last()
        saved_job_post.job_major.set(job_major)
        saved_job_post.job_desc_file = request.FILES.get('job_desc_file')
        saved_job_post.job_requirement_file = request.FILES.get('job_requirement_file')
        saved_job_post.save()
        
        return HttpResponseRedirect(reverse('job_post_index'))
    
    return render(request, 'job_post/create_job_post.html', {
        'job_type_choices': JobPost.job_type_choices,
        'all_companies': Company.objects.all(),
        'all_major': Major.objects.all()
    })
    
def display_job_post(request, job_post_id):
    return render(request, 'job_post/display_job_post.html', {
        'selected_job_post': JobPost.objects.get(pk=job_post_id),
        'all_applicants': JobPost.objects.get(pk=job_post_id).applicants.all(),
        'test': JobPost.objects.get(pk=job_post_id).job_desc_file
    })
    
def edit_job_post(request, job_post_id):

    if request.method == "POST":
        edited_job_post = JobPost.objects.get(pk=job_post_id)
        edited_job_post.job_title = request.POST.get('job_title')
        edited_job_post.job_type = request.POST.get('job_type')
        edited_job_post.company = Company.objects.get(pk=request.POST.get('company'))
        edited_job_post.job_desc_text = request.POST.get('job_desc_text')
        edited_job_post.job_desc_file = request.FILES.get('job_desc_file')
        edited_job_post.job_requirement_text = request.POST.get('job_requirement_text')
        edited_job_post.job_requirement_file = request.FILES.get('job_requirement_file')
        edited_job_post.job_close_date =  request.POST.get('job_close_date')
        edited_job_post.job_location =  request.POST.get('job_location')
        edited_job_post.job_status =  request.POST.get('job_status')
        edited_job_post.job_major.set(Major.objects.filter(pk__in=request.POST.getlist('job_major'))) 
        edited_job_post.save()
        return HttpResponseRedirect(reverse('display_job_post', args=(job_post_id,)))
        
    return render(request, 'job_post/edit_job_post.html', {
        'edited_job_post': JobPost.objects.get(pk=job_post_id),
        'job_type_choices': JobPost.job_type_choices,
        'all_companies': Company.objects.all(),
        'all_major': Major.objects.all(),
        'job_status_choices': JobPost.job_status_choices
    })
    
def update_job_desc_file(request):
    pass
    # if request.method == 'POST':
    #     job_desc_file = request.FILES.get('job_desc_file')
    #     updated_job_post = JobPost.objects
    #     updated_job_post.job_desc_file = file
    #     updated_job_post.save()
    #     return HttpResponse('Upload Photo Succesful')

def update_job_requirement_file(request):
    pass