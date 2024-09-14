from django.db import models
from django.utils.timezone import now
from .storage import OverwriteStorage
from django.utils.deconstruct import deconstructible

import os

from user_profiles.models import *
from company.models import *
# Create your models here.

@deconstructible
class PathRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{instance.id}_{instance}.{ext}'
        return os.path.join(self.path, filename)
        
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
    job_info_file = models.FileField(upload_to=PathRename('job_post/job_info_file'), storage=OverwriteStorage(), null=True, blank=True)
    job_desc_text = models.CharField(max_length=1000, null=True, blank=True)
    job_requirement_text = models.CharField(max_length=1000, null=True, blank=True)
    job_major = models.ManyToManyField(Major, related_name="job_posts_by_major", blank=True)
    job_post_date = models.DateTimeField(default=now)
    job_close_date = models.DateTimeField(null=True, blank=True)
    job_location = models.CharField(max_length=500, null=True, blank=True)
    job_status = models.CharField(choices=job_status_choices, max_length=10, default='active')
    favourite_user = models.ManyToManyField(User, related_name="favourite_posts", blank=True)
    applicants = models.ManyToManyField(Student, related_name="applied_job_posts", blank=True)
    
    def serialize(self):
        if self.company.comp_name_th:

            return {
                'job_id': self.id,
                'job_title': self.job_title,
                'job_type': self.job_type,
                'comp_id': self.company.id,
                'company': self.company.comp_name + '(' + self.company.comp_name_th + ')',
                'company_logo': self.company.comp_logo.url,
                'job_location': self.job_location,
                'job_post_date': self.job_post_date,
                'job_close_date': self.job_close_date,
                'job_status': self.job_status,
            }
        else:
            return {
                'job_id': self.id,
                'job_title': self.job_title,
                'job_type': self.job_type,
                'comp_id': self.company.id,
                'company': self.company.comp_name,
                'company_logo': self.company.comp_logo.url,
                'job_location': self.job_location,
                'job_post_date': self.job_post_date,
                'job_close_date': self.job_close_date,
                'job_status': self.job_status,
            }

    def __str__(self):
        return f"{self.job_title} ({self.company})"
    