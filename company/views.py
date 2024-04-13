import json
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from company.models import *
from user_profiles.models import *
from django.db.models import Q

# Create your views here.
def index(request) :
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        all_companies = Company.objects.filter(
            Q(comp_name__icontains=search_term) |
            Q(comp_desc__icontains=search_term) 
            )
    else:
        all_companies = Company.objects.all()    
    json_string = json.dumps([comp.serialize() for comp in all_companies])
    return render(request, 'company/company_list.html', {
        'all_companies': json_string,
    })

def comp_info(request, comp_id):
     if Employer.objects.filter(user__id = request.user.id).exists():
        return render(request, 'company/compinfo.html', {
                'comp_id': comp_id,
                'isUserEmployer': True
            })
     else:
         return render(request, 'company/compinfo.html', {
                'comp_id': comp_id,
                'isUserEmployer': False
            })

def get_company(request, comp_id):
    company = Company.objects.get(pk = comp_id).serialize()
    return JsonResponse(company, safe=False)

def get_all_company(request):
    all_companies = Company.objects.all()    
    return JsonResponse([comp.serialize() for comp in all_companies], safe=False)

@csrf_exempt
@login_required
@permission_required('user_profiles.is_employer', raise_exception=True)
def update_company(request, comp_id):
    url = reverse('company:comp_info', kwargs={'comp_id': comp_id})
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
@login_required
@permission_required('user_profiles.is_employer', raise_exception=True)
def update_comp_logo(request, comp_id):
    if request.method == 'POST':
        logo = request.FILES.get('comp_logo')
        company = Company.objects.get(pk=comp_id)
        company.comp_logo = logo
        company.save()
        return HttpResponse('Upload Logo Successful')

@login_required
@permission_required('user_profiles.is_employer', raise_exception=True)
def create_company_page(request):
    if request.method == 'POST':
        comp_name = request.POST.get('comp_name')
        comp_desc = request.POST.get('comp_desc')
        logo = request.FILES.get('comp_logo')
        logo.name = comp_name.replace(' ', '_') + '.png'
        print(comp_name, comp_desc, request.FILES.get('comp_logo'))
        company = Company.objects.create(comp_name = comp_name, comp_desc = comp_desc, comp_logo = logo)
        url = reverse('company:comp_info', kwargs={'comp_id': company.id})
        return HttpResponseRedirect(url)
    else:
        return render(request, 'company/create_company.html')

    