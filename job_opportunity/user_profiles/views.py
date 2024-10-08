import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from user_profiles.models import *
from user_profiles.forms import UserForm
from company.views import get_all_company
from django.db.models import Q


# Create your views here.
@login_required(login_url='/user_profiles/')
def index(request,user_id):
    return render(request, 'user_profiles/profile.html', {
        'user_id': user_id,
        'current_user_id': request.user.id,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth.login(request, user)
            if request.user.fname == None:
                return HttpResponseRedirect(reverse("user_profiles:index", kwargs={'user_id': request.user.id}))
            else :

                return HttpResponseRedirect(reverse("job_post:index"))
            
        else:
            return render(request, "user_profiles/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.id:
            return HttpResponse(status=422)
        else:
            return render(request, "user_profiles/login.html")

@login_required(login_url='/user_profiles/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_profiles:login"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]

        if any(domain in email for domain in ['student.chula.ac.th', 'cbs.chula.ac.th']) == False:
            return render(request, "user_profiles/register.html", {
                "message": "Please enter student/cbs email (@student.chula.ac.th or @cbs.chula.ac.th)"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_profiles/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            if 'student.chula.ac.th' in email:
                student = Student.objects.create(user=User.objects.get(email=email))
                student.save()
            elif 'cbs.chula.ac.th' in email:
                professor = Professor.objects.create(user=User.objects.get(email=email))
                professor.save()
        except IntegrityError:
            return render(request, "user_profiles/register.html", {
                "message": "Email already exists."
            })
        auth.authenticate(request, username=username, password=password)
        auth.login(request, user)
        return render(request, "user_profiles/fillinfo.html")
    else:
        return render(request, "user_profiles/register.html")

@csrf_exempt
@login_required(login_url='/user_profiles/')
def fill_info(request) :
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        phone = request.POST['phone']
        major = request.POST['major']

        if not fname or not lname or not phone :
            return render(request, "user_profiles/fillinfo.html", {
                "message": "Please fill all info"
            })
    
        User.objects.filter(pk=request.user.id).update(
            fname = fname,
            lname = lname,
            phone = phone
        )

        if Student.objects.filter(user__id = request.user.id).exists():
            Student.objects.filter(user__id = request.user.id).update(major = Major.objects.get(pk=major))
        elif Professor.objects.filter(user__id = request.user.id).exists():
            Professor.objects.filter(user__id = request.user.id).update(major = Major.objects.get(pk=major))
        return HttpResponseRedirect(reverse("job_post:index"))
    else:
        return render(request, "user_profiles/fillinfo.html")

@login_required(login_url='/user_profiles/')
def get_user(request, user_id):
    user = User.objects.get(pk=user_id).serialize()
    if Student.objects.filter(user__id = user_id).exists():
        student = Student.objects.get(user__id = user_id).serialize()
        user.update(student)
        if Portfolio.objects.filter(student = Student.objects.get(user__id = user_id)).exists():
            file_list = []
            for file in Portfolio.objects.filter(student = Student.objects.get(user__id = user_id)):
                file_list.append(file.serialize())
            user.update({'student_portfolio': file_list})
        return JsonResponse(user, safe=False)
    if Professor.objects.filter(user__id = user_id).exists():
        professor = Professor.objects.filter(user__id = user_id).first().serialize()
        user.update(professor)
        return JsonResponse(user, safe=False)
    elif Employer.objects.filter(user__id = user_id).exists():
        employer = Employer.objects.get(user__id = user_id).serialize()
        user.update(employer)
        return JsonResponse(user, safe=False)
    
@login_required(login_url='/user_profiles/')
def get_major(request):
    majors = Major.objects.all()
    return JsonResponse([major.serialize() for major in majors], safe=False)

@csrf_exempt
@login_required(login_url='/user_profiles/')
def update_user(request):
    url = reverse("user_profiles:index", kwargs={'user_id': request.user.id})
    if request.method == 'POST':
        user = UserForm(request.POST, request.FILES, instance=User.objects.get(pk=request.user.id))
        
        if Student.objects.filter(user__id = request.user.id).exists():
            Student.objects.filter(user__id = request.user.id).update(
                major = request.POST.get('major', '')
            )
        elif Professor.objects.filter(user__id = request.user.id).exists():
            Professor.objects.filter(user__id = request.user.id).update(
                major = request.POST.get('major', '')
            )

        elif Employer.objects.filter(user__id = request.user.id).exists():
            Employer.objects.filter(user__id = request.user.id).update(
                comp= request.POST.get('comp', ''),
                emp_position= request.POST.get('emp_position', '')
            )
        if user.is_valid():
            user.save()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url) 
    
@csrf_exempt
@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_student', raise_exception=True)
def update_student_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('student_resume')
        student = Student.objects.get(user__id = request.user.id)
        student.student_resume = resume
        student.save()
        return HttpResponse('Upload Resume Succesful')

@csrf_exempt
@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_student', raise_exception=True)
def update_student_portfolio(request):
     if request.method == 'POST':
        portfolio = request.FILES.getlist('student_portfolio')
        for file in portfolio:
            file_ins = Portfolio(student= Student.objects.get(user=request.user), student_portfolio = file)
            file_ins.save()
        return HttpResponse('Upload Portfolio Succesful')

@csrf_exempt
@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_student', raise_exception=True)
def remove_student_portfolio(request, file_name):
    Portfolio.objects.filter(student= Student.objects.get(user=request.user), student_portfolio = 'user_profiles/Portfolio/'+file_name).delete()
    return HttpResponse('Remove Portfolio Succesful')

@csrf_exempt
@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_professor', raise_exception=True)
def create_employer(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_profiles/create_employer.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            employer = Employer.objects.create(user=User.objects.get(email=email), prof=Professor.objects.get(user=request.user))
            employer.save()
            return render(request, "user_profiles/create_employer.html", {
                "message": f"Created Account {email}"
            })
        except IntegrityError:
            return render(request, "user_profiles/create_employer.html", {
                "message": "Email already exists."
            })
    return render(request, 'user_profiles/create_employer.html')

@login_required(login_url='/user_profiles/')
@csrf_exempt
def get_company(request):
    return get_all_company(request)

@login_required(login_url='/user_profiles/')
def followed_comp(request):
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        followed_comp = request.user.followed_company.filter(
            Q(comp_name__icontains=search_term) |
            Q(comp_desc__icontains=search_term) 
            )
    else:
        followed_comp = request.user.followed_company.all()   
    return render(request, 'user_profiles/followed_comp.html', {
        'followed_companies': json.dumps([comp.serialize() for comp in followed_comp])
    })