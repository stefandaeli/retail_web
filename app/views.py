from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db.models import Q
from .utilities import ppn
from .decorators import login_required
from datetime import datetime, timedelta, date
from django.db.models import Sum
import json

# Create your views here.

# access utilities function
# def dashboard(request):
#      nilai = 100000
#      hasil = ppn(nilai)
#      return HttpResponse(hasil)

#Login

def superadmin_login(request):
     return render(request, 'login/superadmin_login.html')

def post_superadmin_login(request):
     kode_superadmin = request.POST['kode_superadmin'].upper()
     password_superadmin = request.POST['password_superadmin'].upper()
     
     if SuperAdmins.objects.filter(kode_superadmin=kode_superadmin).exists():
          superadmin = SuperAdmins.objects.get(kode_superadmin=kode_superadmin)
          if password_superadmin == superadmin.password_superadmin:
               #simpan data session
               request.session['nama_superadmin'] = superadmin.nama_superadmin
               request.session['kode_superadmin'] = superadmin.kode_superadmin
               request.session['status_login'] = 'Super Admin'
               request.session.save()
               messages.success(request, 'Berhasil Login !')
               return redirect('dashboard')
          else:
            messages.error(request, 'Password Salah !')
     else:
          #Login untuk admin
          if Admins.objects.filter(kode_admin=kode_superadmin).exists():
               admin = Admins.objects.get(kode_admin=kode_superadmin)
               if password_superadmin == admin.password_admin:
                    #simpan data session
                    request.session['nama_admin'] = admin.nama_admin
                    request.session['kode_admin'] = admin.kode_admin
                    request.session['status_login'] = 'Admin'
                    request.session.save() 
                    messages.error(request, 'Berhasil Login !')
                    return redirect('dashboard')
               else:
                    messages.error(request, 'Password Salah !')
          else:
             messages.error(request, 'Admin Tidak Ditemukan !')  
     return redirect(request.META.get('HTTP_REFERER','/'))

def logout(request):
     request.session.flush()
     messages.success(request, 'Berhasil Logout')
     return redirect('superadmin_login')
#Dashboard

@login_required()
def dashboard(request):
     today = date.today()
     start_of_day = datetime.combine(today, datetime.min.time())
     end_of_day = datetime.combine(today + timedelta(days=1), datetime.min.time()) - timedelta(seconds=1)
     
     jumlah_transaksi_hari_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_day, end_of_day)).count()
     total_data_barang = DataBarang.objects.count()
     total_penjualan_hari_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_day, end_of_day)).aggregate(Sum('grand_total_sales'))['grand_total_sales__sum'] or 0
     
     context = {
         'total_data_barang': total_data_barang,
         'jumlah_transaksi_hari_ini': jumlah_transaksi_hari_ini,
         'total_penjualan_hari_ini': total_penjualan_hari_ini,
     }
      
     return render(request, 'dashboard.html', context)

# Admins

@login_required()
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

@login_required()
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

@login_required()   
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
     return redirect('v_satuanbarang')

# KelompokBarang

def v_kelompokbarang(request):
     data_kelompokbarang = KelompokBarang.objects.all().order_by('kode_kelompok')
     context = {
          'data_kelompokbarang' : data_kelompokbarang
     }
     return render (request, 'kelompok_barang/v_kelompokbarang.html', context)

def add_kelompokbarang(request):
     return render(request, 'kelompok_barang/v_kelompokbarang.html')

def post_add_kelompokbarang(request):
     kode_kelompok = request.POST['kode_kelompok']
     nama_kelompok = request.POST['nama_kelompok']
     timestamp = request.POST['timestamp']
     
     if KelompokBarang.objects.filter(kode_kelompok=kode_kelompok).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
     else : 
          add_kelompokbarang = KelompokBarang(
               kode_kelompok = kode_kelompok,
               nama_kelompok = nama_kelompok,
               timestamp = timestamp
          )
          add_kelompokbarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

def update_kelompokbarang(request, kode_kelompok):
     data_kelompokbarang = KelompokBarang.objects.get(kode_kelompok=kode_kelompok)
     context = {
           'data_kelompokbarang' : data_kelompokbarang
     }
     return render(request, 'kelompok_barang/u_kelompokbarang.html', context)

def post_update_kelompokbarang(request):
     kode_kelompok = request.POST['kode_kelompok']
     nama_kelompok = request.POST['nama_kelompok']
     timestamp = request.POST['timestamp']
     data_kelompokbarang = KelompokBarang.objects.get(kode_kelompok=kode_kelompok)
     
     data_kelompokbarang.nama_kelompok = nama_kelompok
     data_kelompokbarang.timestamp = timestamp
     data_kelompokbarang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_kelompokbarang')

def delete_kelompokbarang(request, kode_kelompok):
     data_kelompokbarang =KelompokBarang.objects.get(kode_kelompok=kode_kelompok).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_kelompokbarang')

# Gudang

def v_gudang(request):
     
     data_gudang = Gudang.objects.all().order_by('kode_gudang')
     context = {
          'data_gudang' : data_gudang
     }
     return render(request, 'gudang/v_gudang.html',context)

def add_gudang(request):
     return render(request,'gudang/v_gudang.html')

def post_add_gudang(request):
     kode_gudang = request.POST['kode_gudang']
     nama_gudang = request.POST['nama_gudang']
     timestamp = request.POST['timestamp']
     
     if Gudang.objects.filter(kode_gudang=kode_gudang).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_gudang = Gudang(
               kode_gudang = kode_gudang,
               nama_gudang = nama_gudang,
               timestamp = timestamp
          )
          data_gudang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

def update_gudang(request, kode_gudang):
     data_gudang = Gudang.objects.get(kode_gudang=kode_gudang)
     context = {
          'data_gudang' : data_gudang
     }
     return render(request,'gudang/u_gudang.html', context)

def post_update_gudang(request):
     kode_gudang = request.POST['kode_gudang']
     nama_gudang = request.POST['nama_gudang']
     timestamp = request.POST['timestamp']
     data_gudang = Gudang.objects.get(kode_gudang=kode_gudang)
     
     data_gudang.nama_gudang = nama_gudang
     data_gudang.timestamp = timestamp
     data_gudang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_gudang')

def delete_gudang(request, kode_gudang):
     data_gudang = Gudang.objects.get(kode_gudang=kode_gudang).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_gudang')

# JenisBarang

def v_jenisbarang(request):
     data_jenisbarang  = JenisBarang.objects.all().order_by('kode_jenis')
     context = {
          'data_jenisbarang' : data_jenisbarang
     }
     return render(request, 'jenis_barang/v_jenisbarang.html',context)

def add_jenisbarang(request):
     return render(request,'jenis_barang/v_jenisbarang.html')

def post_add_jenisbarang(request):
     
     kode_jenis = request.POST['kode_jenis']
     nama_jenis = request.POST['nama_jenis']
     timestamp = request.POST['timestamp']
     
     if JenisBarang.objects.filter(kode_jenis=kode_jenis).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
     else :
          data_jenisbarang = JenisBarang (
               kode_jenis = kode_jenis,
               nama_jenis = nama_jenis,
               timestamp = timestamp
          )
          data_jenisbarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_jenisbarang(request,kode_jenis):
     data_jenisbarang = JenisBarang.objects.get(kode_jenis=kode_jenis)
     context = {
          'data_jenisbarang' : data_jenisbarang
     }
     return render(request,'jenis_barang/u_jenisbarang.html', context)

def post_update_jenisbarang(request):
     kode_jenis = request.POST['kode_jenis']
     nama_jenis = request.POST['nama_jenis']
     timestamp = request.POST['timestamp']
     
     data_jenisbarang = JenisBarang.objects.get(kode_jenis=kode_jenis)
     
     data_jenisbarang.nama_jenis = nama_jenis
     data_jenisbarang.timestamp = timestamp
     data_jenisbarang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_jenisbarang')

def delete_jenisbarang(request,kode_jenis):
     data_jenisbarang = JenisBarang.objects.get(kode_jenis=kode_jenis).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_jenisbarang')

# DataBarang

def v_databarang(request):
     data_barang = DataBarang.objects.all().order_by('kode_barang')
     data_kelompokbarang = KelompokBarang.objects.all().order_by('nama_kelompok')
     data_jenisbarang = JenisBarang.objects.all().order_by('nama_jenis')
     data_satuanbarang = SatuanBarang.objects.all().order_by('nama_satuan')
     context = {
          'data_kelompokbarang' : data_kelompokbarang,
          'data_jenisbarang' : data_jenisbarang,
          'data_satuanbarang' : data_satuanbarang,
          'data_barang' : data_barang
     }
     return render(request,'data_barang/v_databarang.html',context)

def add_databarang(request):
     return render(request,'data_barang/v_databarang.html')

def post_add_databarang(request):
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     kelompok_barang = request.POST['kelompok_barang']
     jenis_barang = request.POST['jenis_barang']
     satuan_barang_small = request.POST['satuan_barang_small']
     satuan_barang_medium = request.POST['satuan_barang_medium']
     satuan_barang_large = request.POST['satuan_barang_large']
     tgl_expire_barang = request.POST['tgl_expire_barang']
     timestamp = request.POST['timestamp']
     
     if DataBarang.objects.filter(kode_barang=kode_barang).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          databarang = DataBarang(
               kode_barang = kode_barang,
               nama_barang = nama_barang,
               kelompok_barang = kelompok_barang,
               jenis_barang = jenis_barang,
               satuan_barang_small = satuan_barang_small,
               satuan_barang_medium = satuan_barang_medium,
               satuan_barang_large = satuan_barang_large,
               tgl_expire_barang = tgl_expire_barang,
               timestamp= timestamp
          )
          databarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

def update_databarang(request, kode_barang):
     data_barang = DataBarang.objects.get(kode_barang=kode_barang)
     data_kelompokbarang = KelompokBarang.objects.all().order_by('nama_kelompok')
     data_jenisbarang = JenisBarang.objects.all().order_by('nama_jenis')
     data_satuanbarang = SatuanBarang.objects.all().order_by('nama_satuan')
     context = {
          'data_kelompokbarang' : data_kelompokbarang,
          'data_jenisbarang' : data_jenisbarang,
          'data_satuanbarang' : data_satuanbarang,
          'data_barang' : data_barang
     }
     return render(request, 'data_barang/u_databarang.html',context)

def post_update_databarang(request):
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     kelompok_barang = request.POST['kelompok_barang']
     jenis_barang = request.POST['jenis_barang']
     satuan_barang_small = request.POST['satuan_barang_small']
     satuan_barang_medium = request.POST['satuan_barang_medium']
     satuan_barang_large = request.POST['satuan_barang_large']
     tgl_expire_barang = request.POST['tgl_expire_barang']
     timestamp = request.POST['timestamp']
     
     data_barang = DataBarang.objects.get(kode_barang=kode_barang)
     data_barang.nama_barang = nama_barang
     data_barang.kelompok_barang = kelompok_barang
     data_barang.jenis_barang = jenis_barang
     data_barang.satuan_barang_small = satuan_barang_small
     data_barang.satuan_barang_medium = satuan_barang_medium
     data_barang.satuan_barang_large = satuan_barang_large
     data_barang.tgl_expire_barang = tgl_expire_barang
     data_barang.timestamp = timestamp
     data_barang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_databarang')

def delete_databarang(request, kode_barang):
     data_barang = DataBarang.objects.get(kode_barang=kode_barang).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_databarang')

# StokBarang

def v_stokbarang(request):
     data_stokbarang = StokBarang.objects.all().order_by('kode_stok')
     data_gudang = Gudang.objects.all().order_by('nama_gudang')
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     context = {
          'data_stokbarang' : data_stokbarang,
          'data_gudang' : data_gudang,
          'data_barang' : data_barang,
     }
     return render(request,'stok_barang/v_stokbarang.html',context)

def add_stokbarang(request):
     return render(request, 'stok_barang/v_stok_barang.html')

def post_add_stokbarang(request):
     kode_stok = request.POST['kode_stok']
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     stok_satuan_small = request.POST['stok_satuan_small']
     stok_satuan_medium = request.POST['stok_satuan_medium']
     stok_satuan_large = request.POST['stok_satuan_large']
     nama_gudang = request.POST['nama_gudang']
     timestamp = request.POST['timestamp']
     
     if StokBarang.objects.filter(kode_stok=kode_stok).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
     else :
          data_stokbarang = StokBarang (
               kode_stok = kode_stok,
               kode_barang = kode_barang,
               # mengambil salah satu value :
               nama_barang = nama_barang.split(',')[0],
               stok_satuan_small =stok_satuan_small,
               stok_satuan_medium = stok_satuan_medium,
               stok_satuan_large = stok_satuan_large,
               nama_gudang = nama_gudang,
               timestamp = timestamp
          )
          data_stokbarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_stokbarang(request, kode_stok):
     data_stokbarang = StokBarang.objects.get(kode_stok=kode_stok)
     data_gudang = Gudang.objects.all().order_by('nama_gudang')
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     context = {
          'data_stokbarang' : data_stokbarang,
          'data_gudang' : data_gudang,
          'data_barang' : data_barang
     }
     return render(request, 'stok_barang/u_stokbarang.html',context)

def post_update_stokbarang(request):
     kode_stok = request.POST['kode_stok']
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     stok_satuan_small = request.POST['stok_satuan_small']
     stok_satuan_medium = request.POST['stok_satuan_medium']
     stok_satuan_large = request.POST['stok_satuan_large']
     nama_gudang = request.POST['nama_gudang']
     timestamp = request.POST['timestamp']
     
     data_stokbarang = StokBarang.objects.get(kode_stok=kode_stok)
     data_stokbarang.kode_barang = kode_barang
     data_stokbarang.nama_barang = nama_barang
     data_stokbarang.stok_satuan_small = stok_satuan_small
     data_stokbarang.stok_satuan_medium = stok_satuan_medium
     data_stokbarang.stok_satuan_large = stok_satuan_large
     data_stokbarang.nama_gudang = nama_gudang
     data_stokbarang.timestamp = timestamp
     
     data_stokbarang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_stokbarang')

def delete_stokbarang(request, kode_stok):
     data_stokbarang = StokBarang.objects.get(kode_stok=kode_stok).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_stokbarang')

# HargaBarang

def v_hargabarang(request):
     data_hargabarang = HargaBarang.objects.all().order_by('kode_harga')
     data_barang = DataBarang.objects.all().order_by('kode_barang')
     
     context = {
          'data_hargabarang' : data_hargabarang,
          'data_barang' : data_barang
     }
     return render(request,'harga_barang/v_hargabarang.html',context)

def add_hargabarang(request):
     return render(request,'harga_barang/v_hargabarang')

def post_add_hargabarang(request):
     kode_harga = request.POST['kode_harga']
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     harga_satuan_small = request.POST['harga_satuan_small']
     harga_satuan_medium = request.POST['harga_satuan_medium']
     harga_satuan_large = request.POST['harga_satuan_large']
     ppn_barang = request.POST['ppn_barang']
     diskon_barang = request.POST['diskon_barang']
     timestamp = request.POST['timestamp']
     
     if HargaBarang.objects.filter(kode_harga=kode_harga).exists():
          messages.error(request, 'Kode sudah digunakan !')
          return redirect(request.META.get('HTTP_REFERER','/'))
            
     else :
          data_hargabarang = HargaBarang(
               kode_harga = kode_harga,
               kode_barang = kode_barang,
               nama_barang = nama_barang.split(',')[0],
               harga_satuan_small = harga_satuan_small,
               harga_satuan_medium = harga_satuan_medium,
               harga_satuan_large = harga_satuan_large,
               ppn_barang = ppn_barang,
               diskon_barang =diskon_barang,
               timestamp = timestamp
          )
          data_hargabarang.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_hargabarang(request, kode_harga):
     data_hargabarang = HargaBarang.objects.get(kode_harga=kode_harga)
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     
     context = {
          'data_hargabarang' : data_hargabarang,
          'data_barang' : data_barang
     }
     return render(request,'harga_barang/u_hargabarang.html',context)
     
def post_update_hargabarang(request):
     kode_harga = request.POST['kode_harga']
     kode_barang = request.POST['kode_barang']
     nama_barang = request.POST['nama_barang']
     harga_satuan_small = request.POST['harga_satuan_small']
     harga_satuan_medium = request.POST['harga_satuan_medium']
     harga_satuan_large = request.POST['harga_satuan_large']
     ppn_barang = request.POST['ppn_barang']
     diskon_barang = request.POST['diskon_barang']
     timestamp = request.POST['timestamp']
     
     data_hargabarang = HargaBarang.objects.get(kode_harga=kode_harga)
     data_hargabarang.kode_barang = kode_barang
     data_hargabarang.nama_barang = nama_barang
     data_hargabarang.harga_satuan_small = harga_satuan_small
     data_hargabarang.harga_satuan_medium = harga_satuan_medium
     data_hargabarang.harga_satuan_large = harga_satuan_large
     data_hargabarang.ppn_barang = ppn_barang
     data_hargabarang.diskon_barang = diskon_barang
     data_hargabarang.timestamp = timestamp
     data_hargabarang.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_hargabarang')

def delete_hargabarang(request, kode_harga):
     data_hargabarang = HargaBarang.objects.get(kode_harga=kode_harga).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_hargabarang')

# JenisCustomers

def v_jeniscustomers(request):
     data_jeniscustomers = JenisCustomers.objects.all().order_by("kode_jenis_customers")
     context = {
          'data_jeniscustomers' : data_jeniscustomers
     }
     return render(request,'jenis_customers/v_jeniscustomers.html',context)

def add_jeniscustomers(request):
     return render(request,'jenis_customers/v_jeniscustomers.html')

def post_add_jeniscustomer(request):
     kode_jenis_customers = request.POST['kode_jenis_customers']
     nama_jenis_customers = request.POST['nama_jenis_customers']
     timestamp = request.POST['timestamp']
     
     if JenisCustomers.objects.filter(kode_jenis_customers=kode_jenis_customers).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_jeniscustomers = JenisCustomers(
               kode_jenis_customers = kode_jenis_customers,
               nama_jenis_customers = nama_jenis_customers,
               timestamp = timestamp
          )
          data_jeniscustomers.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_jeniscustomers(request, kode_jenis_customers):
     data_jeniscustomers = JenisCustomers.objects.get(kode_jenis_customers=kode_jenis_customers)
     context = {
          'data_jeniscustomers' : data_jeniscustomers
     }
     return render(request,'jenis_customers/u_jeniscutomers.html',context)

def post_update_jeniscustomers(request):
     kode_jenis_customers = request.POST['kode_jenis_customers']
     nama_jenis_customers = request.POST['nama_jenis_customers']
     timestamp = request.POST['timestamp']
     
     data_jeniscustomers = JenisCustomers.objects.get(kode_jenis_customers=kode_jenis_customers)
     data_jeniscustomers.nama_jenis_customers =nama_jenis_customers
     data_jeniscustomers.timestamp = timestamp
     
     data_jeniscustomers.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_jeniscustomers')

def delete_jeniscustomers(request, kode_jenis_customers):
     data_jeniscustomers = JenisCustomers.objects.get(kode_jenis_customers=kode_jenis_customers).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_jeniscustomers')

# Customers
     
def v_customers(request):
     data_customers = Customers.objects.all().order_by('kode_customers')
     data_jeniscustomers = JenisCustomers.objects.all().order_by('kode_jenis_customers')
     context = {
          'data_customers' : data_customers,
          'data_jeniscustomers' : data_jeniscustomers
     }
     return render(request,'customers/v_customers.html',context)

def post_add_customers(request):
     kode_customers = request.POST['kode_customers']
     nama_customers = request.POST['nama_customers']
     jenis_customers = request.POST['jenis_customers']
     alamat_customers = request.POST['alamat_customers']
     wa_customer = request.POST['wa_customer']
     email_customers = request.POST['email_customers']
     timestamp = request.POST['timestamp']
     
     if Customers.objects.filter(kode_customers=kode_customers).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_customers = Customers(
               kode_customers = kode_customers,
               nama_customers = nama_customers,
               jenis_customers = jenis_customers,
               alamat_customers = alamat_customers,
               wa_customer = wa_customer,
               email_customers =email_customers,
               timestamp = timestamp
          )
          data_customers.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_customers(request,kode_customers):
     data_customers = Customers.objects.get(kode_customers=kode_customers)
     data_jeniscustomers = JenisCustomers.objects.all().order_by('nama_jenis_customers')
     context = {
          'data_customers' : data_customers,
          'data_jeniscustomers' : data_jeniscustomers
     }
     return render(request, 'customers/u_customers.html',context)

def post_update_customers(request):
     kode_customers = request.POST['kode_customers']
     nama_customers = request.POST['nama_customers']
     jenis_customers = request.POST['jenis_customers']
     alamat_customers = request.POST['alamat_customers']
     wa_customer = request.POST['wa_customer']
     email_customers = request.POST['email_customers']
     timestamp = request.POST['timestamp']
     
     data_customers = Customers.objects.get(kode_customers=kode_customers)
     data_customers.nama_customers = nama_customers
     data_customers.jenis_customers = jenis_customers
     data_customers.alamat_customers = alamat_customers
     data_customers.wa_customer = wa_customer
     data_customers.email_customers = email_customers
     data_customers.timestamp = timestamp
     data_customers.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_customers')

def delete_customers(request, kode_customers):
     data_customers = Customers.objects.get(kode_customers=kode_customers).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_customers')

# Sopir

def v_sopir(request):
     data_sopir = Sopir.objects.all().order_by('kode_sopir')
     context = {
          'data_sopir' : data_sopir
     }
     return render(request,'sopir/v_sopir.html',context)

def post_add_sopir(request):
     kode_sopir = request.POST['kode_sopir']
     nama_sopir = request.POST['nama_sopir']
     alamat_sopir = request.POST['alamat_sopir']
     wa_sopir = request.POST['wa_sopir']
     email_sopir = request.POST['email_sopir']
     timestamp = request.POST['timestamp']
     
     if Sopir.objects.filter(kode_sopir=kode_sopir).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_sopir = Sopir(
               kode_sopir = kode_sopir,
               nama_sopir = nama_sopir,
               alamat_sopir = alamat_sopir,
               wa_sopir = wa_sopir,
               email_sopir = email_sopir,
               timestamp = timestamp
          )
          data_sopir.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_sopir(request, kode_sopir):
     data_sopir  = Sopir.objects.get(kode_sopir=kode_sopir)
     context = {
          'data_sopir' : data_sopir
     }
     return render(request,'sopir/u_sopir.html',context)

def post_update_sopir(request):
     kode_sopir = request.POST['kode_sopir']
     nama_sopir = request.POST['nama_sopir']
     alamat_sopir = request.POST['alamat_sopir']
     wa_sopir = request.POST['wa_sopir']
     email_sopir = request.POST['email_sopir']
     timestamp = request.POST['timestamp']
     
     data_sopir = Sopir.objects.get(kode_sopir=kode_sopir)
     data_sopir.nama_sopir = nama_sopir
     data_sopir.alamat_sopir = alamat_sopir
     data_sopir.wa_sopir = wa_sopir
     data_sopir.email_sopir = email_sopir
     data_sopir.timestamp = timestamp
     data_sopir.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_sopir')

def delete_sopir(request,kode_sopir):
     data_sopir = Sopir.objects.get(kode_sopir=kode_sopir).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_sopir')

# SalesTransactions

def v_salestransactions(request):
     data_sales = SalesTransactions.objects.all().order_by('kode_sales')
     context = {
          'data_sales' : data_sales
     }
     return render(request,'sales_transactions/v_salestransactions.html',context)

def add_salestransactions(request):
     data_sales = SalesTransactions.objects.all().order_by('kode_sales')
     data_customers = Customers.objects.all().order_by('nama_customers')
     data_sopir = Sopir.objects.all().order_by('nama_sopir')
     data_barang = DataBarang.objects.all().order_by('kode_barang')
     data_hargabarang = HargaBarang.objects.all().order_by('kode_harga')
     merged_data = []

     for barang, harga_barang in zip(data_barang, data_hargabarang):
        merged_data.append({
            'kode_barang': barang.kode_barang,
            'nama_barang': barang.nama_barang,
            'satuan_barang_small' : barang.satuan_barang_small,
            'satuan_barang_medium' : barang.satuan_barang_medium,
            'satuan_barang_large' : barang.satuan_barang_large,
            'harga_satuan_small': harga_barang.harga_satuan_small,
            'harga_satuan_medium' : harga_barang.harga_satuan_medium,
            'harga_satuan_large': harga_barang.harga_satuan_large
     })
     context = {
          'data_sales' : data_sales,
          'data_customers' : data_customers,
          'data_sopir' : data_sopir,
          'data_mergebarang' : merged_data
     }
     return render(request,'sales_transactions/add_salestransactions.html',context)

def post_add_salestransactions(request):
     kode_sales = request.POST['kode_sales']
     nama_customers = request.POST['nama_customers']
     kode_customers = request.POST['kode_customers']
     nama_sopir = request.POST['nama_sopir']
     kode_sopir = request.POST['kode_sopir']
     nama_barang = request.POST['nama_barang']
     kode_barang = request.POST['kode_barang']
     nama_satuan = request.POST['nama_satuan']
     harga_barang = request.POST['harga_barang']
     quantity_sales = request.POST['quantity_sales']
     diskon_sales = request.POST['diskon_sales']
     biaya_pengiriman = request.POST['biaya_pengiriman']
     sub_total_sales = request.POST['sub_total_sales']
     grand_total_sales = request.POST['grand_total_sales']
     jenis_pembayaran = request.POST['jenis_pembayaran']
     total_pembayaran_sales = request.POST['total_pembayaran_sales']
     sisa_tagihan = request.POST['sisa_tagihan']
     status = request.POST['status']
     timestamp = request.POST['timestamp']
     
     if SalesTransactions.objects.filter(kode_sales=kode_sales).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_sales = SalesTransactions (
               kode_sales = kode_sales,
               nama_customers =nama_customers,
               kode_customers = kode_customers,
               nama_sopir = nama_sopir,
               kode_sopir = kode_sopir,
               nama_barang = nama_barang.split(';'),
               kode_barang = kode_barang,
               nama_satuan = nama_satuan,
               harga_barang = harga_barang,
               quantity_sales = quantity_sales,
               diskon_sales = diskon_sales,
               biaya_pengiriman = biaya_pengiriman,
               sub_total_sales = sub_total_sales,
               grand_total_sales = grand_total_sales,
               jenis_pembayaran = jenis_pembayaran,
               total_pembayaran_sales = total_pembayaran_sales,
               sisa_tagihan = sisa_tagihan,
               status = status,
               timestamp = timestamp
          )
          data_sales.save()
          # item_values = nama_barang.split('|')
          # kode = item_values[0]
          # nama = item_values[1]
          # description = item_values[2]
          # quantity = int(item_values[4])

          # try:
          #     with SalesTransactions.atomic():
          #         stok = StokBarang.objects.get(kode_barang=kode, stok_satuan_small=description)
          #         # Pastikan stok tidak menjadi negatif
          #         if stok.stok_satuan_small - quantity >= 0:
          #             stok.stok_satuan_small -= quantity
          #             stok.save()
          #         else:
          #             # Handle kasus ketika pengurangan stok membuat nilai negatif
          #             # Misalnya, lemparkan exception atau lakukan tindakan yang sesuai
          #             pass
          # except StokBarang.DoesNotExist:
          #     # Handle ketika objek tidak ditemukan
          #     pass
          # except StokBarang.MultipleObjectsReturned:
          #     # Handle ketika lebih dari satu objek ditemukan
          #     pass
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

# DataSupplier

def v_datasupplier(request):
     data_supplier = DataSupplier.objects.all().order_by('kode_supplier')   
     context = {
          'data_supplier' : data_supplier
     }
     return render(request,'supplier/v_datasupplier.html',context)

def add_datasupplier(request):
     return render(request,'supplier/add_datasupplier.html')

def post_add_datasupplier(request):
     kode_supplier = request.POST['kode_supplier']
     nama_supplier = request.POST['nama_supplier']
     alamat_supplier = request.POST['alamat_supplier']
     npwp_supplier = request.POST['npwp_supplier']
     tlp_supplier = request.POST['tlp_supplier']
     email_supplier = request.POST['email_supplier']
     wa_supplier = request.POST['wa_supplier']
     nama_bank_supplier = request.POST['nama_bank_supplier']
     no_rek_supplier = request.POST['no_rek_supplier']
     ket_supplier = request.POST['ket_supplier']
     status_aktif_supplier = request.POST['status_aktif_supplier']
     timestamp = request.POST['timestamp']
     
     if DataSupplier.objects.filter(kode_supplier=kode_supplier).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_supplier = DataSupplier(
               kode_supplier = kode_supplier,
               nama_supplier = nama_supplier,
               alamat_supplier = alamat_supplier,
               npwp_supplier = npwp_supplier,
               tlp_supplier = tlp_supplier,
               email_supplier = email_supplier,
               wa_supplier = wa_supplier,
               nama_bank_supplier = nama_bank_supplier,
               no_rek_supplier = no_rek_supplier,
               ket_supplier = ket_supplier,
               status_aktif_supplier = status_aktif_supplier,
               timestamp = timestamp,
          )
          data_supplier.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))

def update_datasupplier(request,kode_supplier):
     data_supplier = DataSupplier.objects.get(kode_supplier=kode_supplier)
     context = {
          'data_supplier' : data_supplier
     }
     return render(request, 'supplier/u_datasupplier.html',context)
     
def post_update_datasupplier(request):
     kode_supplier = request.POST['kode_supplier']
     nama_supplier = request.POST['nama_supplier']
     alamat_supplier = request.POST['alamat_supplier']
     npwp_supplier = request.POST['npwp_supplier']
     tlp_supplier = request.POST['tlp_supplier']
     email_supplier = request.POST['email_supplier']
     wa_supplier = request.POST['wa_supplier']
     nama_bank_supplier = request.POST['nama_bank_supplier']
     no_rek_supplier = request.POST['no_rek_supplier']
     ket_supplier = request.POST['ket_supplier']
     status_aktif_supplier = request.POST['status_aktif_supplier']
     timestamp = request.POST['timestamp']
     
     data_supplier = DataSupplier.objects.get(kode_supplier=kode_supplier)
     data_supplier.nama_supplier = nama_supplier
     data_supplier.alamat_supplier = alamat_supplier
     data_supplier.npwp_supplier = npwp_supplier
     data_supplier.tlp_supplier = tlp_supplier
     data_supplier.email_supplier = email_supplier
     data_supplier.wa_supplier = wa_supplier
     data_supplier.nama_bank_supplier = nama_bank_supplier
     data_supplier.no_rek_supplier = no_rek_supplier
     data_supplier.ket_supplier = ket_supplier
     data_supplier.status_aktif_supplier = status_aktif_supplier
     data_supplier.timestamp = timestamp
     data_supplier.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_datasupplier')
     
def delete_datasupplier(request,kode_supplier):
     DataSupplier.objects.get(kode_supplier=kode_supplier).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_datasupplier')

# BarangSupplier

def v_barangsupplier(request):
     data_barangsupplier = BarangSupplier.objects.select_related('kode_supplier').all()
     context = {
          'data_barangsupplier' : data_barangsupplier
     }
     return render(request,'barangsupplier/v_barangsupplier.html',context)
