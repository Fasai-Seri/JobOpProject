from django.db import models
from .storage import OverwriteStorage
from django.utils.deconstruct import deconstructible
import os

# Create your models here.

@deconstructible
class PathRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{instance.id}_{instance}.{ext}'
        return os.path.join(self.path, filename)
    
class Company(models.Model):
    comp_name = models.CharField(max_length=100, null=True)
    comp_name_th = models.CharField(max_length=100, null=True, blank=True)
    comp_desc = models.CharField(max_length=1000, null=True)
    comp_logo = models.ImageField(upload_to=PathRename('company/Images'), storage=OverwriteStorage(), default='company/Images/default.jpg', null=True)
    comp_address = models.CharField(max_length=1000, null=True)
    comp_long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    comp_lat  = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    comp_contact_info = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return f"{self.comp_name}"
    
    def serialize(self) :
        if self.comp_logo:
            return {
                'comp_id': self.id,
                'comp_name': self.comp_name,
                'comp_name_th': self.comp_name_th,
                'comp_desc': self.comp_desc,
                'comp_logo': self.comp_logo.url[1:],
                'comp_address': self.comp_address,
                'comp_long': str(self.comp_long),
                'comp_lat': str(self.comp_lat),
                'comp_contact_info': self.comp_contact_info,
            }
        else:
            return {
                'comp_id': self.id,
                'comp_name': self.comp_name,
                'comp_name_th': self.comp_name_th,
                'comp_desc': self.comp_desc,
                'comp_address': self.comp_address,
                'comp_long': str(self.comp_long),
                'comp_lat': str(self.comp_lat),
                'comp_contact_info': self.comp_contact_info,
            }