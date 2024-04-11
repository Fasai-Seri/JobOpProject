from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from company.models import *

# Create your views here.
def index(request) :
    return render(request, '')

def comp_info(request, comp_id):
    return render(request, 'company/compinfo.html', {
            'comp_id': comp_id
        })

def get_company(request, comp_id):
    company = Company.objects.get(pk = comp_id).serialize()
    return JsonResponse(company, safe=False)