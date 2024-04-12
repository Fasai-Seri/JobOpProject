from django.db import models
from django.utils.timezone import now

from user_profiles.models import *
from company.models import *
# Create your models here.

class JobPost(models.Model):
    
    job_type_choices = (
        ("internship", "Internship"),
        ("part time", "Part Time"),
        ("full time", "Full Time")
    )
    
    job_status_choices = (
        ("active", "Active"),
        ("inactive", "Inactive")
    )
    
    poster_emp = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_posted_by_emp', null=True, blank=True)
    poster_prof = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='job_posted_by_prof', null=True, blank=True)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(choices=job_type_choices, max_length=10, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job_posts_by_company", default='')
    job_desc_text = models.CharField(max_length=1000, null=True, blank=True)
    job_desc_file = models.FileField(upload_to='static/job_post/files', null=True, blank=True)
    job_requirement_text = models.CharField(max_length=1000, null=True, blank=True)
    job_requirement_file = models.FileField(upload_to='static/job_post/files', null=True, blank=True)
    job_major = models.ManyToManyField(Major, related_name="job_posts_by_major")
    job_post_date = models.DateTimeField(default=now)
    job_close_date = models.DateTimeField(null=True, blank=True)
    job_location = models.CharField(max_length=500, null=True, blank=True)
    job_status = models.CharField(choices=job_status_choices, max_length=10, default='')
    favourite_user = models.ManyToManyField(User, related_name="favourite_posts", blank=True)
    applicants = models.ManyToManyField(Student, related_name="applied_job_posts", blank=True)
    
    def __str__(self):
        return f"{self.job_title} ({self.company})"
    