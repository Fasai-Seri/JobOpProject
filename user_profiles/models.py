from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(validators=[MinLengthValidator(10)], max_length=10, null=True)
    pass
class Major(models.Model):
    major_id = models.CharField(validators=[MinLengthValidator(3)], max_length=3, primary_key=True)
    major_desc = models.CharField(max_length=100, null=True)
    pass
class Professor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prof_user_id')
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='prof_major_id')
    pass

class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    comp_logo = models.ImageField(upload_to='static/user_profiles/Images')
    pass

class Employer(models.Model):
    prof_id = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='approve_prof_id')
    comp_id = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='comp_id')
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='emp_user_id')
    emp_position = models.CharField(max_length=100, null=True)
    pass
class Student(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_user_id')
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='student_major_id')
    student_resume = models.FileField(upload_to='static/user_profiles/Files')
    pass