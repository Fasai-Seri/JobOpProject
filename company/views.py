import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from company.models import *
from user_profiles.models import *
from job_post.models import *
from django.db.models import Q
from job_post.views import toggle_favorite
from company.forms import CompanyForm

# Create your views here.
@login_required(login_url='/user_profiles/')
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

    if Employer.objects.filter(user__id = request.user.id).exists():
        return render(request, 'company/company_list.html', {
        'all_companies': json_string,
        'isUserEmployer': True,
    })
    else:
         return  render(request, 'company/company_list.html', {
        'all_companies': json_string,
        'isUserEmployer': False,
    })

@login_required(login_url='/user_profiles/')
def comp_info(request, comp_id):
     if Employer.objects.filter(user__id = request.user.id, comp__id = comp_id).exists():
        return render(request, 'company/compinfo.html', {
                'comp_id': comp_id,
                'canEdit': True,
            })
     else:
         return render(request, 'company/compinfo.html', {
                'comp_id': comp_id,
                'canEdit': False
            })

@login_required(login_url='/user_profiles/')
def get_company(request, comp_id):
    company = Company.objects.get(pk = comp_id).serialize()
    company.update({
        'isFollowedByUser': Company.objects.get(pk = comp_id) in request.user.followed_company.all()
    })
    return JsonResponse(company, safe=False)

@login_required(login_url='/user_profiles/')
def get_company_job_posts(request, comp_id):
    jobpost_list = []
    for post in JobPost.objects.filter(company__id = comp_id).order_by('job_status', '-job_post_date'):
        jobpost = post.serialize()
        jobpost.update({'isFavorite': post in request.user.favourite_posts.all()})
        jobpost_list.append(jobpost)
    return JsonResponse(jobpost_list, safe=False)

@login_required(login_url='/user_profiles/')
def get_all_company(request):
    all_companies = Company.objects.all()    
    return JsonResponse([comp.serialize() for comp in all_companies], safe=False)

@csrf_exempt
@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_employer', raise_exception=True)
def update_company(request, comp_id):
    url = reverse('company:comp_info', kwargs={'comp_id': comp_id})
    if request.method == 'POST':
        company = CompanyForm(request.POST, request.FILES, instance=Company.objects.get(pk=comp_id))
        if company.is_valid():
            company.save()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)

@login_required(login_url='/user_profiles/')
@permission_required('user_profiles.is_employer', raise_exception=True)
def create_company_page(request):
    if request.method == 'POST':
        logo = request.FILES.get('comp_logo')
        comp_name = request.POST.get('comp_name')
        comp_name_th = request.POST.get('comp_name_th')
        comp_desc = request.POST.get('comp_desc')
        comp_address = request.POST.get('comp_address')
        comp_long = request.POST.get('comp_long')
        comp_lat = request.POST.get('comp_lat')
        comp_contact_info = request.POST.get('comp_contact_info')
        company = Company.objects.create(comp_name = comp_name, comp_name_th=comp_name_th, comp_desc = comp_desc, comp_address=comp_address,comp_long = comp_long, comp_lat = comp_lat,comp_contact_info=comp_contact_info)
        if logo :
            logo.name = comp_name.replace(' ', '_') + '.png'
            company.comp_logo = logo
            company.save()
        url = reverse('company:comp_info', kwargs={'comp_id': company.id})
        return HttpResponseRedirect(url)
    else:
        return render(request, 'company/create_company.html')

@login_required(login_url='/user_profiles/')
def follow_company(request, comp_id):
    url = reverse("company:comp_info", kwargs={'comp_id': comp_id})
    comp = Company.objects.get(pk=comp_id)
    user = request.user
    if comp in user.followed_company.all():
        user.followed_company.remove(comp)
    else:
        user.followed_company.add(comp)
    return HttpResponseRedirect(url)

@login_required(login_url='/user_profiles/')
def favorite(request, post_id):
    toggle_favorite(request, post_id)
    return HttpResponse('Fav Triggered')