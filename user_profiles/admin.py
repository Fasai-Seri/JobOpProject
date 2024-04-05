from django.contrib import admin
from user_profiles.models import User, Major, Company

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Company)
admin.site.register(Major)
admin.site.register(Employer)
admin.site.register(Student)
