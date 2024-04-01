from django.db import models
from user_profiles.models import Employer, Professor
# Create your models here.

class JobPost(models.Model):
    emp_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_posted_emp', blank=True)
    prof_id = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='job_posted_prof', blank=True)
    post_title = models.CharField(max_length=100)
    post_desc = models.CharField(max_length=1000)
    post_posted_date = models.DateField()
    post_status = models.BooleanField()