from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from company.models import Company

# Create your models here.

class User(AbstractUser):
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(validators=[MinLengthValidator(10)], max_length=10, null=True)
    user_photo = models.ImageField(upload_to='user_profiles/Images', null=True, blank=True)
    followed_company = models.ManyToManyField(Company, related_name="following_user", blank=True)
    
    def serialize(self):
        if self.user_photo:
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
    def __str__(self):
        return f"{self.username}"
class Major(models.Model):
    major_id = models.CharField(validators=[MinLengthValidator(3)], max_length=3, primary_key=True)
    major_desc = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            'id': self.major_id,
            'desc': self.major_desc
        }
        
    def __str__(self):
        return f"{self.major_desc}"
class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prof_user_id', null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='prof_major_id', null=True)
    
    def serialize(self):
        return {
            'major': self.major.major_id,
            'type': 'professor'
        }
        
    def __str__(self):
        return f"{self.user}"
    
class Employer(models.Model):
    prof = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name='approve_prof_id', null=True)
    comp = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='comp_id', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='emp_user_id', null=True)
    emp_position = models.CharField(max_length=100, null=True, blank=True)
    def serialize(self):
        if self.comp:
            return {
                'prof': self.prof.user.id,
                'comp': self.comp.id,
                'emp_position': self.emp_position,
                'type': 'employer'
            }
        else:
            return {
                'prof': self.prof.user.id,
                'comp': '',
                'emp_position': self.emp_position,
                'type': 'employer'
            }
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_user_id', null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='student_major_id', null=True)
    student_resume = models.FileField(upload_to='user_profiles/Files', null=True, blank=True)
    def serialize(self):
        if self.student_resume:
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