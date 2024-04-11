import json
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

@csrf_exempt
def update_company(request, comp_id):
    url = reverse(comp_info, kwargs={'comp_id': comp_id})
    if request.method == 'POST':
        data = json.loads(request.body)
        Company.objects.filter(pk=comp_id).update(
            comp_name = data.get('comp_name', ''),
            comp_desc = data.get('comp_desc', ''),
        )
        print(data)

        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)

@csrf_exempt
def update_comp_logo(request, comp_id):
    if request.method == 'POST':
        logo = request.FILES.get('comp_logo')
        company = Company.objects.get(pk=comp_id)
        company.comp_logo = logo
        company.save()
        return HttpResponse('Upload Logo Successful')
