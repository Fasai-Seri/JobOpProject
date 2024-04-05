from django.db import models
from user_profiles.models import *
# Create your models here.

class JobPost(models.Model):
    job_type_choices = {
        "Intern": "internship",
        "Part Time": "part time",
        "Full Time": "full time"
    }
    poster_emp_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_posted_emp', blank=True)
    poster_prof_id = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='job_posted_prof', blank=True)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=job_type_choices)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job_posts_by_company")
    job_desc = models.CharField(max_length=1000, blank=True)
    job_requirements = models.CharField(max_length=1000, blank=True)
    job_major = models.ManyToManyField(Major, related_name="job_posts_by_major", blank=True)
    job_posted_date = models.DateField(max_length=500)
    job_close_date = models.DateField(blank=True)
    job_location = models.CharField(max_length=)
    job_status = models.BooleanField()
    favourite_user = models.ManyToManyField(User, related_name="fovourit_posts", blank=True)
    