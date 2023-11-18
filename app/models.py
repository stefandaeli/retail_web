from django.db import models

# Create your models here.
class Admins(models.Model):
    kode_admin = models.CharField(max_length=20,primary_key=True)
    nama_admin = models.CharField(max_length=50)
    password_admin = models.CharField(max_length=20)
    
