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


# Create your views here.
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
            print(request.user.has_perm('user_profiles.is_professor'))
            print('login')
            if request.user.fname == None:
                print('fname blank')
                return HttpResponseRedirect(reverse("job_post:index", kwargs={'user_id': request.user.id}))
            else :
                print('fname not blank')
                return HttpResponseRedirect(reverse("job_post:index"))
            
        else:
            return render(request, "user_profiles/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user:
            return HttpResponse(status=422)
        else:
            return render(request, "user_profiles/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("job_post:index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]

        if any(domain in email for domain in ['student.chula.ac.th', 'cbs.chula.ac.th']) == False:
            return render(request, "user_profiles/register.html", {
                "message": "Please enter student/cbs email"
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
        login(request, user)
        return render(request, "user_profiles/fillinfo.html")
    else:
        return render(request, "user_profiles/register.html")

@csrf_exempt
@login_required
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
            Student.objects.filter(user__id = request.user.id).update(major = Major.objects.get(pk=major))
        return HttpResponseRedirect(reverse("job_post:index"))
    else:
        return render(request, "user_profiles/fillinfo.html")
    
def get_user(request, user_id):
    user = User.objects.get(pk=user_id).serialize()
    if Student.objects.filter(user__id = user_id).exists():
        student = Student.objects.get(user__id = user_id).serialize()
        user.update(student)
        return JsonResponse(user, safe=False)
    if Professor.objects.filter(user__id = user_id).exists():
        professor = Professor.objects.filter(user__id = user_id).first().serialize()
        user.update(professor)
        return JsonResponse(user, safe=False)
    elif Employer.objects.filter(user__id = user_id).exists():
        employer = Employer.objects.get(user__id = user_id).serialize()
        user.update(employer)
        return JsonResponse(user, safe=False)
    
def get_major(request):
    majors = Major.objects.all()
    return JsonResponse([major.serialize() for major in majors], safe=False)

@csrf_exempt
@login_required
def update_user(request):
    url = reverse("job_post:index", kwargs={'user_id': request.user.id})
    if request.method == 'POST':
        data = json.loads(request.body)
        user = UserForm(data, instance=User.objects.get(pk=request.user.id))

        if Student.objects.filter(user__id = request.user.id).exists():
            Student.objects.filter(user__id = request.user.id).update(
                major = data.get('major', '')
            )
        elif Professor.objects.filter(user__id = request.user.id).exists():
            Professor.objects.filter(user__id = request.user.id).update(
                major = data.get('major', '')
            )

        elif Employer.objects.filter(user__id = request.user.id).exists():
            print(data.get('comp', ''))
            Employer.objects.filter(user__id = request.user.id).update(
                comp= data.get('comp', ''),
                emp_position= data.get('emp_position', '')
            )

        if user.is_valid():
            user.save()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url) 

@csrf_exempt
@login_required
def update_user_photo(request):
    if request.method == 'POST':
        photo = request.FILES.get('user_photo')
        user=request.user
        user.user_photo = photo
        user.save()
        return HttpResponse('Upload Photo Succesful')
    
@csrf_exempt
@login_required
@permission_required('user_profiles.is_student', raise_exception=True)
def update_student_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('student_resume')
        print(resume)
        student = Student.objects.get(user__id = request.user.id)
        student.student_resume = resume
        student.save()
        return HttpResponse('Upload Resume Succesful')

@csrf_exempt
@login_required
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

def get_company(request):
    return get_all_company(request)
