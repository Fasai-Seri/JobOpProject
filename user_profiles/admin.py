from django.contrib import admin
from user_profiles.models import User, Major, Company

from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ('following_user',)
    
admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Major)
admin.site.register(Employer)
admin.site.register(Student)
