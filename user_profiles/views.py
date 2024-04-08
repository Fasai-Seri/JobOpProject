import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user_profiles.models import *

# Create your views here.
def index(request,user_id):
    return render(request, 'user_profiles/profile.html', {
        'user_id': user_id
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_profiles/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "user_profiles/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
                student = Student.objects.create(user_id=User.objects.get(email=email))
                student.save()
            elif 'cbs.chula.ac.th' in email:
                professor = Professor.objects.create(user_id=User.objects.get(email=email))
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

        if Student.objects.filter(user_id__id = request.user.id).first():
            Student.objects.filter(user_id__id = request.user.id).update(major_id = Major.objects.get(pk=major))
        elif Professor.objects.filter(user_id__id = request.user.id).first():
            Student.objects.filter(user_id__id = request.user.id).update(major_id = Major.objects.get(pk=major))
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "user_profiles/fillinfo.html")
    
def get_user(request, user_id):
    user = User.objects.get(pk=user_id).serialize()
    if Student.objects.filter(user_id__id = user_id).first():
        student = Student.objects.get(user_id__id = user_id).serialize()
        user.update(student)
        return JsonResponse(user, safe=False)
    if Professor.objects.filter(user_id__id = user_id).first():
        professor = Professor.objects.filter(user_id__id = user_id).first().serialize()
        user.update(professor)
        return JsonResponse(user, safe=False)
    elif Employer.objects.filter(user_id__id = user_id).first():
        employer = Employer.objects.get(user_id__id = user_id).serialize()
        user.update(employer)
        return JsonResponse(user, safe=False)
    
def get_major(request):
    majors = Major.objects.all()
    return JsonResponse([major.serialize() for major in majors], safe=False)

def get_user_type(request, user_id):
    if Student.objects.get(user_id__id = user_id):
        return JsonResponse({'user_type': 'student'}, safe=False)
    elif Professor.objects.get(user_id__id = user_id):
        return JsonResponse({'user_type': 'professor'}, safe=False)
    elif Employer.objects.get(user_id__id = user_id):
        return JsonResponse({'user_type': 'employer'}, safe=False)