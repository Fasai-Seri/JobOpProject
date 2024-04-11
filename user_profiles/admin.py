from django.contrib import admin
from user_profiles.models import User, Major

from .models import *
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ('followed_company',)

admin.site.register(User, CompanyAdmin)
admin.site.register(Professor)
admin.site.register(Major)
admin.site.register(Employer)
admin.site.register(Student)
