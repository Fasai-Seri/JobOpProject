from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(validators=[MinLengthValidator(10)], max_length=10, null=True)
    user_photo = models.ImageField(upload_to='static/user_profiles/Images', null=True, blank=True)
    
    def serialize(self):
        if self.user_photo != '':
            return {
                'email': self.email,
                'fname': self.fname,
                'lname':self.lname,
                'phone':self.phone,
                'user_photo': self.user_photo.url[1:],
            }
        else:
            return {
                'email': self.email,
                'fname': self.fname,
                'lname':self.lname,
                'phone':self.phone,
            }

class Major(models.Model):
    major_id = models.CharField(validators=[MinLengthValidator(3)], max_length=3, primary_key=True)
    major_desc = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            'id': self.major_id,
            'desc': self.major_desc
        }
class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prof_user_id', null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='prof_major_id', null=True)
    
    def serialize(self):
        return {
            'major': self.major.major_id,
            'type': 'professor'
        }

class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    comp_logo = models.ImageField(upload_to='static/user_profiles/Images', default='static/user_profiles/Images/default.jpg', null=True)
    pass

class Employer(models.Model):
    prof = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='approve_prof_id', null=True)
    comp = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='comp_id', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='emp_user_id', null=True)
    emp_position = models.CharField(max_length=100, null=True)
    def serialize(self):
        return {
            'prof': self.prof,
            'comp': self.comp,
            'emp_position': self.emp_position,
            'type': 'employer'
        }
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_user_id', null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='student_major_id', null=True)
    student_resume = models.FileField(upload_to='static/user_profiles/Files', null=True, blank=True)
    def serialize(self):
        if self.student_resume != '':
            return {
                'major': self.major.major_id,
                'type': 'student',
                'resume': self.student_resume.url[1:],
            }
        else:
             return {
                'major': self.major.major_id,
                'type': 'student',
            }