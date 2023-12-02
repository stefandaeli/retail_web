from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Admins, SatuanBarang, KelompokBarang, Gudang
from .models import JenisBarang, DataBarang, StokBarang, HargaBarang
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