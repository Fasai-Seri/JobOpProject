from django.db import models
from django.utils.timezone import now

from user_profiles.models import *
# Create your models here.

class JobPost(models.Model):
    
    job_type_choices = (
        ("internship", "Intern"),
        ("part time", "Part Time"),
        ("full time", "full Time")
    )
    
    job_status_choices = (
        ("active", "Active"),
        ("inactive", "Inactive")
    )
    
    poster_emp = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_posted_emp', null=True)
    poster_prof = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='job_posted_prof', null=True)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=job_type_choices, max_length=10, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job_posts_by_company", default='')
    job_desc = models.CharField(max_length=1000, null=True)
    job_requirements = models.CharField(max_length=1000, null=True)
    job_major = models.ManyToManyField(Major, related_name="job_posts_by_major")
    job_posted_date = models.DateTimeField(default=now)
    job_close_date = models.DateTimeField(null=True)
    job_location = models.CharField(max_length=500, null=True)
    job_status = models.CharField(choices=job_status_choices, max_length=10, default='')
    favourite_user = models.ManyToManyField(User, related_name="fovourite_posts")
    