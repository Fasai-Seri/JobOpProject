from django.contrib import admin

from .models import *
# Register your models here.

class JobPostAdmin(admin.ModelAdmin):
    filter_horizontal = ('job_major', 'favourite_user',)
    
admin.site.register(JobPost, JobPostAdmin)