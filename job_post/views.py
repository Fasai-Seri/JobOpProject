from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.urls import reverse
from datetime import date
from io import BytesIO
import datetime

from .models import *
# Create your views here.

def is_student(user):
    return Student.objects.filter(user=user).first()

def is_professor(user):
    return Professor.objects.filter(user=user).first()

def is_employer(user):
    return Employer.objects.filter(user=user).first()

def is_permitted_poster(user):
    return is_professor(user) or is_employer(user)

def is_job_post_owner(user, job_post_id):
    selected_job_post = JobPost.objects.get(pk=job_post_id)
    if selected_job_post.poster_emp is not None:
        return selected_job_post.poster_emp.user == user
    else:
        return selected_job_post.poster_prof.user == user

def job_post_with_search_term(all_job_posts, search_term):
    filtered_job_posts = all_job_posts.filter(
        Q(job_title__icontains=search_term) |
        Q(job_type__icontains=search_term) |
        Q(job_desc_text__icontains=search_term) |
        Q(job_requirement_text__icontains=search_term) |
        Q(job_location__icontains=search_term) |
        Q(job_status__icontains=search_term) |
        Q(company__comp_name__icontains=search_term) |
        Q(company__comp_desc__icontains=search_term) 
    )
    return filtered_job_posts

def convert_username_to_year(username):
    current_year = date.today().year + 543
    if date.today().month > 6:
        current_year += 1
    entering_year = int(username[:2]) + 2500
    return current_year - entering_year

@login_required    
def index(request):
    all_job_posts = JobPost.objects.all() 
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = job_post_with_search_term(all_job_posts, search_term)
           
    return render(request, 'job_post/index.html', {
        'all_job_posts': all_job_posts,
        'job_type_choices': JobPost.job_type_choices,
        'all_major': Major.objects.all(),
        'job_status_choices': JobPost.job_status_choices,
    })

@login_required      
def favourite(request):
    all_job_posts = request.user.favourite_posts.all() 
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = job_post_with_search_term(all_job_posts, search_term)
        
    return render(request, 'job_post/favourite.html', {
        'all_job_posts': all_job_posts,
    })

@login_required      
def following(request):
    all_job_posts = JobPost.objects.filter(company__in=request.user.followed_company.all())
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_job_posts = job_post_with_search_term(all_job_posts, search_term)
        
    return render(request, 'job_post/following.html', {
        'all_job_posts': all_job_posts,
        'followed_companies': request.user.followed_company.all()
    })

@login_required      
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

@login_required  
def create_job_post(request):
    if is_permitted_poster(request.user):
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
                                job_location = job_location,
                                job_status = job_status
                                )
            if Employer.objects.filter(user_id=request.user):
                poster_emp = Employer.objects.filter(user_id=request.user).first()
                new_job_post.poster_emp = poster_emp
            elif Professor.objects.filter(user_id=request.user):
                poster_prof = Professor.objects.filter(user_id=request.user).first()
                new_job_post.poster_prof = poster_prof
                
            if job_close_date != '':
                new_job_post.job_close_date = job_close_date
                
            new_job_post.save()
            
            saved_job_post = JobPost.objects.last()
            saved_job_post.job_major.set(job_major)
            saved_job_post.job_desc_file = request.FILES.get('job_desc_file')
            saved_job_post.job_requirement_file = request.FILES.get('job_requirement_file')
            saved_job_post.save()
            
            return HttpResponseRedirect(reverse('job_post:index'))
        
        return render(request, 'job_post/create_job_post.html', {
            'job_type_choices': JobPost.job_type_choices,
            'all_companies': Company.objects.all(),
            'all_major': Major.objects.all()
        })
        
    return render(request, 'job_post/create_job_post.html', {
            'warning': "Your account doesn't have permission to access this page"
    })
    

@login_required      
def display_job_post(request, job_post_id):
    return render(request, 'job_post/display_job_post.html', {
        'selected_job_post': JobPost.objects.get(pk=job_post_id),
        'all_applicants': JobPost.objects.get(pk=job_post_id).applicants.all(),
        'is_job_post_owner': is_job_post_owner(request.user, job_post_id),
        'is_student': is_student(request.user)
    })

@login_required      
def edit_job_post(request, job_post_id):
    if is_job_post_owner(request.user, job_post_id):
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
            return HttpResponseRedirect(reverse('job_post:display_job_post', args=(job_post_id,)))
            
        return render(request, 'job_post/edit_job_post.html', {
            'edited_job_post': JobPost.objects.get(pk=job_post_id),
            'job_type_choices': JobPost.job_type_choices,
            'all_companies': Company.objects.all(),
            'all_major': Major.objects.all(),
            'job_status_choices': JobPost.job_status_choices
        })
        
    return render(request, 'job_post/edit_job_post.html', {
            'warning': "Your account doesn't have permission to access this page"
    })

@login_required
def posted_job_posts(request):
   
    if is_permitted_poster(request.user):
        
        if is_employer(request.user):
            all_job_posts = request.user.emp_user_id.get().job_posted_by_emp.all()
        else:
            all_job_posts = request.user.prof_user_id.get().job_posted_by_prof.all()
            
        if request.GET.get('search_term'):
            search_term = request.GET.get('search_term')
            all_job_posts = job_post_with_search_term(all_job_posts, search_term)
            
        return render(request, 'job_post/posted_job_posts.html', {
            'all_job_posts': all_job_posts
        })
        
    return render(request, 'job_post/posted_job_posts.html', {
        'warning': "Your account doesn't have permission to access this page"
    })

@login_required   
def applied_job_posts(request):
    
    if is_student(request.user):
        
        all_job_posts = request.user.student_user_id.get().applied_job_posts.all()
            
        if request.GET.get('search_term'):
            search_term = request.GET.get('search_term')
            all_job_posts = job_post_with_search_term(all_job_posts, search_term)
            
        return render(request, 'job_post/applied_job_posts.html', {
            'all_job_posts': all_job_posts
        })
        
    return render(request, 'job_post/applied_job_posts.html', {
        'warning': "Your account doesn't have permission to access this page"
    })


def generate_pdf(request, job_post_id):
    response = FileResponse(generate_pdf_file(job_post_id), 
                            as_attachment=True, 
                            filename='applicants.pdf')
    return response 

def generate_pdf_file(job_post_id):
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    selected_job_post = JobPost.objects.get(pk=job_post_id)
    p.setFont('Helvetica-Bold',12)
    p.drawString(100, 750, f"Applicants of {selected_job_post}")
    
    p.setFont('Helvetica', 10)
    all_applicants = selected_job_post.applicants.all()
    y = 700
    i = 1
    for applicant in all_applicants:
        if i % 7 == 1 and i != 1:
            p.showPage()
            y = 750
            p.setFont('Helvetica', 10)
        p.drawString(100, y, f"{str(i)+'.':<4}Name: {applicant.user.fname} {applicant.user.lname} (Year {convert_username_to_year(applicant.user.username)})")
        p.drawString(100, y - 20, f"{'':5}Email: {applicant.user.username}")
        p.drawString(100, y - 40, f"{'':5}Phone: {applicant.user.phone}")
        p.drawString(100, y - 60, f"{'':5}Major: {applicant.major}")
        # p.drawString(100, y - 80, f"{'':5}Resume: {applicant.student_resume}")
        y -= 90
        i += 1
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer