from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admins, SatuanBarang
from django.contrib import messages
from django.db.models import Q
from .utilities import ppn

# Create your views here.

# access utilities function
# def dashboard(request):
#      nilai = 100000
#      hasil = ppn(nilai)
#      return HttpResponse(hasil)

def dashboard(request):
     return render(request, 'dashboard.html')

# Admins

def v_admins(request):
#     read_admins=Admins.objects.filter(kode_admin = 'A0001')
#     read_admins=Admins.objects.filter(kode_admin__icontains='kode_admin')
#     read_admins=Admins.objects.filter(kode_admin='A0001',nama_admin='test')
#     read_admins=Admins.objects.filter(Q(kode_admin='A0001') | Q(nama_admin='test'))
     data_admins=Admins.objects.all().order_by('kode_admin')
     context = {
          'data_admins' : data_admins
     }
     return render(request,'admin/v_admins.html', context)

def add_admins(request):
     return render(request, 'admin/v_admin.html')

def post_add_admins(request):
    kode_admin = request.POST['kode_admin']
    nama_admin = request.POST['nama_admin']
    password_admin = request.POST['password_admin']
    timestamp = request.POST['timestamp']
    
    
    if Admins.objects.filter(kode_admin=kode_admin).exists():
         messages.error(request, 'Kode sudah digunakan !')
         return redirect(request.META.get('HTTP_REFERER','/'))
    else :
          add_admins = Admins(
               kode_admin = kode_admin,
               nama_admin = nama_admin,
               password_admin = password_admin,
               timestamp = timestamp
          )
          add_admins.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_admins(request,kode_admin):
     data_admins=Admins.objects.get(kode_admin=kode_admin)
     context = {
          'data_admins' : data_admins
     }
     return render(request, 'admin/u_admins.html',context)

def post_update_admins(request):
     kode_admin = request.POST['kode_admin']
     nama_admin = request.POST['nama_admin']
     password_admin = request.POST['password_admin']
     timestamp = request.POST['timestamp']
     data_admins=Admins.objects.get(kode_admin=kode_admin)
     
     data_admins.nama_admin = nama_admin
     data_admins.password_admin = password_admin
     data_admins.timestamp = timestamp
     data_admins.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_admins')

def delete_admins(request, kode_admin):
     data_admins=Admins.objects.get(kode_admin=kode_admin).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_admins')

# SatuanBarang

def v_satuanbarang(request):
     data_satuanbarang=SatuanBarang.objects.all().order_by('kode_satuan')
     context = {
          'data_satuanbarang' : data_satuanbarang
     }
     
     return render(request, 'satuan_barang/v_satuanbarang.html', context)

def add_satuanbarang(request):
     return render(request, 'satuan_barang/v_satuanbarang.html')

def post_add_satuanbarang(request):
     kode_satuan = request.POST['kode_satuan']
     nama_satuan = request.POST['nama_satuan']
     timestamp = request.POST['timestamp']
     
     if SatuanBarang.objects.filter(kode_satuan=kode_satuan).exists():
          messages.error(request,'Kode sudah digunakan')
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          add_satuanbarang = SatuanBarang(
               kode_satuan = kode_satuan,
               nama_satuan = nama_satuan,
               timestamp = timestamp
          )
          add_satuanbarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

def update_satuanbarang(request,kode_satuan):
     data_satuanbarang = SatuanBarang.objects.get(kode_satuan=kode_satuan)
     context = {
          'data_satuanbarang' : data_satuanbarang
     }
     return render(request, 'satuan_barang/u_satuanbarang.html',context)


def post_update_satuanbarang(request):
     kode_satuan = request.POST['kode_satuan']
     nama_satuan = request.POST['nama_satuan']
     timestamp = request.POST['timestamp']
     data_satuanbarang = SatuanBarang.objects.get(kode_satuan=kode_satuan)
     
     data_satuanbarang.nama_satuan = nama_satuan 
     data_satuanbarang.timestamp = timestamp
     data_satuanbarang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_satuanbarang')
     
def delete_satuanbarang(request, kode_satuan):
     data_admins=SatuanBarang.objects.get(kode_satuan=kode_satuan).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_admins')
