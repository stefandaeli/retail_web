from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admins
from django.contrib import messages

# Create your views here.
def index(request):
    context ={
         'nama' : 'stefan daeli'
    }
    return render(request,'admin/index.html', context)

def add_admins(request):
     return render(request, 'admin/index.html')

def post_add_admins(request):
    kode_admin = request.POST['kode_admin']
    nama_admin = request.POST['nama_admin']
    password_admin = request.POST['password_admin']
    
    if Admins.objects.filter(kode_admin=kode_admin).exists():
         messages.error(request, 'Kode sudah digunakan !')
         return redirect(request.META.get('HTTP_REFERER','/'))
    else :
          add_admins = Admins(
               kode_admin = kode_admin,
               nama_admin = nama_admin,
               password_admin = password_admin
          )
          add_admins.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))