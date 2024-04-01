from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Professor(AbstractUser):
    prof_fname = models.CharField(max_length=100, null=True)
    prof_lname = models.CharField(max_length=100, null=True)
    prof_phone = models.CharField(min_length=10, max_length=10, null=True)
    pass

class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    pass

class Major(models.Model):
    major_id = models.CharField(min_length=3, max_length=3, primary_key=True)
    major_desc = models.CharField(max_length=100, null=True)
    pass
class Employer(AbstractUser):
    prof_id = models.ForeignKey(Professor)
    comp_id = models.ForeignKey(Company)
    emp_fname = models.CharField(max_length=100, null=True)
    emp_lname = models.CharField(max_length=100, null=True)
    emp_phone = models.CharField(min_length=10, max_length=10, null=True)
    emp_position = models.CharField(max_length=100, null=True)
    pass
class Student(AbstractUser):
    student_fname = models.CharField(max_length=100, null=True)
    student_lname = models.CharField(max_length=100, null=True)
    student_phone = models.CharField(min_length=10, max_length=100, null=True)
    student_resume = models.FileField(upload_to='')
    pass