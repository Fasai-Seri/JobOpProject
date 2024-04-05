from django.contrib import admin
from user_profiles.models import User, Major, Company

# Register your models here.
admin.site.register(Major)
admin.site.register(Company)
admin.site.register(User)