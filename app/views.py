from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db.models import Q
from .utilities import ppn
from .decorators import login_required
from datetime import datetime, timedelta, date
from django.db.models import Sum
import json
from openpyxl import Workbook
from pytz import utc
import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models.functions import TruncMonth
from django.http import FileResponse
import os
from io import BytesIO
import base64
from django.template import loader
from django.utils import timezone
from django.db import transaction
from decimal import Decimal

#Retail
def v_retail(request):
     data_retail = Retails.objects.all()
     context ={
          'data_retail' : data_retail
     }
     return render(request,'v_retail.html',context)

def post_update_retail(request):
     kode_retail = request.POST['kode_retail']
     nama_retail = request.POST['nama_retail']
     alamat_retail = request.POST['alamat_retail']
     wa_retail = request.POST['wa_retail']
     desc_retail = request.POST['desc_retail']
     
     data_retail = Retails.objects.get(kode_retail=kode_retail)
     data_retail.nama_retail = nama_retail
     data_retail.alamat_retail = alamat_retail
     data_retail.wa_retail = wa_retail
     data_retail.desc_retail = desc_retail
     data_retail.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_retail')
     

# Profile

def profile_superadmin(request):
     superadmin = SuperAdmins.objects.get(kode_superadmin=request.session.get('kode_superadmin'))
     data_superadmin = SuperAdmins.objects.filter(kode_superadmin=superadmin.kode_superadmin)
     
     context = {
          'data_superadmin' : data_superadmin
     }
     return render(request,'profile_superadmin.html',context)
     
#Covert To Excel

def detail_barang_excel(request):
     # Membuat workbook dan worksheet
    wb = Workbook()
    ws = wb.active

    # Menambahkan header ke worksheet
    ws.append(['Detail Barang'])
    ws.append(['Kode', 'Nama Barang', 'Kelompok Barang', 'Jenis Barang', 'Satuan Barang Kecil',
               'Tanggal Expire', 'Stok Barang',
               'Nama Gudang', 'Harga Barang', 'PPN Barang', 'Diskon Barang', 'Timestamp'])

    # Mengambil data dari tiga tabel
    data_barang = DataBarang.objects.all()
    stok_barang = StokBarang.objects.all()
    harga_barang = HargaBarang.objects.all()

    # Menggunakan dictionary untuk menyimpan harga barang berdasarkan kode
    harga_barang_dict = {}
    for harga in harga_barang:
        harga_barang_dict[harga.kode_barang] = {
            'harga_satuan_small': harga.harga_satuan_small,
          #   'harga_satuan_medium': harga.harga_satuan_medium,
          #   'harga_satuan_large': harga.harga_satuan_large,
            'ppn_barang' : harga.ppn_barang,
            'diskon_barang' : harga.diskon_barang
        }

    # Iterasi melalui data barang dan menambahkannya ke worksheet
    for barang in data_barang:
        stok = stok_barang.filter(kode_barang=barang.kode_barang).first()
        harga = harga_barang_dict.get(barang.kode_barang, {})

        # Handling datetime.date without timezone info
        tgl_expire_barang = barang.tgl_expire_barang if barang.tgl_expire_barang else None
        timestamp = barang.timestamp if barang.timestamp else None

        # Menghapus informasi zona waktu dari objek datetime jika diperlukan
        if hasattr(tgl_expire_barang, 'astimezone'):
            tgl_expire_barang = tgl_expire_barang.astimezone(utc).replace(tzinfo=None)
        if hasattr(timestamp, 'astimezone'):
            timestamp = timestamp.astimezone(utc).replace(tzinfo=None)

        ws.append([
            barang.kode_barang,
            barang.nama_barang,
            barang.kelompok_barang,
            barang.jenis_barang,
            barang.satuan_barang_small,
          #   barang.satuan_barang_medium,
          #   barang.satuan_barang_large,
            tgl_expire_barang,
            stok.stok_satuan_small if stok else '',
          #   stok.stok_satuan_medium if stok else '',
          #   stok.stok_satuan_large if stok else '',
            stok.nama_gudang if stok else '',
            harga.get('harga_satuan_small', ''),
          #   harga.get('harga_satuan_medium', ''),
          #   harga.get('harga_satuan_large', ''),
            harga.get('ppn_barang', ''),
            harga.get('diskon_barang', ''),
            timestamp,
        ])
      
        

    # Membuat response HTTP
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=detail_barang.xlsx'
    
    # Simpan file Excel
    wb.save(response)

    return response

def transaksi_penjualan_excel(request):
    # Buat workbook dan aktifkan worksheet
    wb = Workbook()
    ws = wb.active

    # Tambahkan judul worksheet
    ws.append(['Transaksi Penjualan'])

    # Tambahkan header kolom
    ws.append(['Kode Transaksi', 'Customer', 'Sopir', 'Grand Total', 'Status', 'Dibayar',
               'Sisa Tagihan', 'Timestamp'])

    # Ambil data transaksi penjualan dari model
    data_sales_transaction = SalesTransactions.objects.all()

    # Tambahkan data ke worksheet
    for transaction in data_sales_transaction:
        # Convert to timezone-aware datetime and then remove timezone information
        timestamp = transaction.timestamp.astimezone(timezone.utc).replace(tzinfo=None)

        ws.append([
            transaction.kode_sales,
            transaction.nama_customers,
            transaction.nama_sopir,
            transaction.grand_total_sales,
            transaction.status,
            transaction.total_pembayaran_sales,
            transaction.sisa_tagihan,
            timestamp,
        ])

    # Buat response HttpResponse
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=sales_transaction.xlsx'

    # Simpan file Excel ke response
    wb.save(response)

    return response
     
     

# Create your views here.

# access utilities function
# def dashboard(request):
#      nilai = 100000
#      hasil = ppn(nilai)
#      return HttpResponse(hasil)

#Login

def superadmin_login(request):
     data_retail = Retails.objects.all()
     context = {
          'data_retail' : data_retail
     }
     return render(request, 'login/superadmin_login.html',context)

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
     today = timezone.now()
     start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
     end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    
     
     jumlah_transaksi_hari_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_day, end_of_day)).count()
     total_data_barang = DataBarang.objects.count()
     total_penjualan_hari_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_day, end_of_day)).aggregate(Sum('grand_total_sales'))['grand_total_sales__sum'] or 0
     
     total_penjualan_per_bulan = SalesTransactions.objects.filter(timestamp__range=(start_of_month, end_of_month)).aggregate(Sum('grand_total_sales'))['grand_total_sales__sum'] or 0
     total_uang_masuk_hari_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_day, end_of_day)).aggregate(Sum('total_pembayaran_sales'))['total_pembayaran_sales__sum'] or 0
     total_uang_masuk_bulan_ini = SalesTransactions.objects.filter(timestamp__range=(start_of_month, end_of_month)).aggregate(Sum('total_pembayaran_sales'))['total_pembayaran_sales__sum'] or 0
     sisa_tagihan = SalesTransactions.objects.filter(timestamp__range=(start_of_month,end_of_month)).aggregate(Sum('sisa_tagihan'))['sisa_tagihan__sum'] or 0
     

     context = {
         'total_data_barang': total_data_barang,
         'jumlah_transaksi_hari_ini': jumlah_transaksi_hari_ini,
         'total_penjualan_hari_ini': total_penjualan_hari_ini,
         'total_penjualan_per_bulan':total_penjualan_per_bulan,
         'total_uang_masuk_hari_ini' : total_uang_masuk_hari_ini,
         'total_uang_masuk_bulan_ini' : total_uang_masuk_bulan_ini,
         'sisa_tagihan' : sisa_tagihan

     }
      
     return render(request, 'dashboard.html', context)

#Superadmins

def post_update_superadmins(request):
     kode_superadmin = request.POST['kode_superadmin']
     nama_superadmin = request.POST['nama_superadmin']
     password_superadmin = request.POST['password_superadmin']
     data_superadmin = SuperAdmins.objects.get(kode_superadmin=kode_superadmin)
     
     data_superadmin.nama_superadmin = nama_superadmin
     data_superadmin.password_superadmin = password_superadmin
     data_superadmin.save()
     messages.success(request, 'Berhasil update data')
     return redirect('profile_superadmin')
     

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

#DetailBarang

def detail_barang(request):
    # Mengambil data dari tiga tabel
    data_barang = DataBarang.objects.all()
    stok_barang = StokBarang.objects.all()
    harga_barang = HargaBarang.objects.all()

    # Gabungkan data menggunakan primary key (kode_barang)
    merged_data = []

    for barang in data_barang:
        stok = stok_barang.filter(kode_barang=barang.kode_barang)
        harga = harga_barang.filter(kode_barang=barang.kode_barang)

        if stok.exists() and harga.exists():
            # Ambil semua objek yang sesuai dari stok dan harga
            stok_data = list(stok.values())
            harga_data = list(harga.values())

            # Gabungkan data stok dan harga menjadi satu dictionary
            merged_data.append({
                'kode_barang': barang.kode_barang,
                'nama_barang': barang.nama_barang,
                'kelompok_barang': barang.kelompok_barang,
                'jenis_barang': barang.jenis_barang,
                'satuan_barang_small': barang.satuan_barang_small,
                'satuan_barang_medium': barang.satuan_barang_medium,
                'satuan_barang_large': barang.satuan_barang_large,
                'tgl_expire_barang': barang.tgl_expire_barang,
                'timestamp': barang.timestamp,
                'stok_satuan_small': stok_data[0]['stok_satuan_small'],  # Misalkan mengambil data pertama
                'stok_satuan_medium': stok_data[0]['stok_satuan_medium'],
                'stok_satuan_large': stok_data[0]['stok_satuan_large'],
                'nama_gudang': stok_data[0]['nama_gudang'],
                'harga_satuan_small': harga_data[0]['harga_satuan_small'],
                'harga_satuan_medium': harga_data[0]['harga_satuan_medium'],
                'harga_satuan_large': harga_data[0]['harga_satuan_large'],
                'ppn_barang': harga_data[0]['ppn_barang'],
                'diskon_barang': harga_data[0]['diskon_barang'],
            })

    context = {
        'merged_data': merged_data,
    }

    return render(request, 'data_barang/detail_barang.html', context)


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
     # satuan_barang_medium = request.POST['satuan_barang_medium']
     # satuan_barang_large = request.POST['satuan_barang_large']
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
               # satuan_barang_medium = satuan_barang_medium,
               # satuan_barang_large = satuan_barang_large,
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
     # harga_satuan_medium = request.POST['harga_satuan_medium']
     # harga_satuan_large = request.POST['harga_satuan_large']
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
               # harga_satuan_medium = harga_satuan_medium,
               # harga_satuan_large = harga_satuan_large,
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
     data_satuan = SatuanBarang.objects.all().order_by('nama_satuan')
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
          'data_mergebarang' : merged_data,
          'data_satuan' : data_satuan
     }
     return render(request,'sales_transactions/add_salestransactions.html',context)

def post_add_salestransactions(request):
    kode_sales = request.POST['kode_sales']
    nama_customers = request.POST['nama_customers']
    kode_customers = request.POST['kode_customers']
    nama_sopir = request.POST['nama_sopir']
    kode_sopir = request.POST['kode_sopir']
    kode_barang_list = request.POST.getlist('kode_barang[]')
    nama_satuan_list = request.POST.getlist('nama_satuan[]')
    harga_barang_list = request.POST.getlist('harga_barang[]')
    quantity_sales_list = request.POST.getlist('quantity_sales[]')
    diskon_sales = request.POST['diskon_sales']
    biaya_pengiriman = request.POST['biaya_pengiriman']
    sub_total_sales = request.POST['sub_total_sales']
    grand_total_sales = request.POST['grand_total_sales']
    jenis_pembayaran = request.POST['jenis_pembayaran']
    total_pembayaran_sales = request.POST['total_pembayaran_sales']
    tagihan_awal = request.POST['sisa_tagihan']
    sisa_tagihan = request.POST['sisa_tagihan']
    status = request.POST['status']
    timestamp = request.POST['timestamp']

    if SalesTransactions.objects.filter(kode_sales=kode_sales).exists():
        messages.error(request, "Kode sudah ada!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        with transaction.atomic():
            data_sales = SalesTransactions(
                kode_sales=kode_sales,
                nama_customers=nama_customers,
                kode_customers=kode_customers,
                nama_sopir=nama_sopir,
                kode_sopir=kode_sopir,
                diskon_sales=diskon_sales,
                biaya_pengiriman=biaya_pengiriman,
                sub_total_sales=sub_total_sales,
                grand_total_sales=grand_total_sales,
                jenis_pembayaran=jenis_pembayaran,
                total_pembayaran_sales=total_pembayaran_sales,
                tagihan_awal = tagihan_awal,
                sisa_tagihan=sisa_tagihan,
                status=status,
                timestamp=timestamp
            )
            data_sales.save()

            for i in range(len(kode_barang_list)):
                data_barang, created = DataBarang.objects.get_or_create(kode_barang=kode_barang_list[i])
                DetailTransaksi.objects.create(
                    kode_sales=data_sales,
                    kode_barang=data_barang,
                    nama_satuan=nama_satuan_list[i],
                    harga_barang=harga_barang_list[i],
                    quantity_sales=quantity_sales_list[i],
                )

                my_model_instances = StokBarang.objects.filter(kode_barang=kode_barang_list[i])
                for instance in my_model_instances:
                    quantity_sales = int(quantity_sales_list[i])
                    if instance.stok_satuan_small >= quantity_sales:
                        instance.stok_satuan_small -= quantity_sales
                        instance.save()
                    else:
                        messages.success(request, 'Stock kurang')
                        return redirect('v_salestransactions')

    messages.success(request, 'Berhasil tambah data')
    return redirect('v_salestransactions')

def delete_salestransactions(request,kode_sales):
     data_sales = SalesTransactions.objects.get(kode_sales=kode_sales).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_salestransactions')
     
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
     data_supplier = DataSupplier.objects.all().order_by('nama_supplier')
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     data_barangsupplier = BarangSupplier.objects.select_related('kode_supplier').all()
     context = {
          'data_barangsupplier' : data_barangsupplier,
          'data_supplier' : data_supplier,
          'data_barang' : data_barang
     }
     return render(request,'barangsupplier/v_barangsupplier.html',context)

def post_add_barangsupplier(request):
     kode_supplier = request.POST['kode_supplier']
     kode_barang = request.POST['kode_barang']
     quantity_satuan_small = request.POST['quantity_satuan_small']
     quantity_satuan_medium = request.POST['quantity_satuan_medium']
     quantity_satuan_large = request.POST['quantity_satuan_large']
     satuan_harga_small = request.POST['satuan_harga_small']
     satuan_harga_medium = request.POST['satuan_harga_medium']
     satuan_harga_large = request.POST['satuan_harga_large']
     timestamp = request.POST['timestamp']
     data_supplier, created = DataSupplier.objects.get_or_create(kode_supplier=kode_supplier)
     data_barang, created = DataBarang.objects.get_or_create(kode_barang=kode_barang)

     if DataBarang.objects.filter(kode_barang=data_barang).exists():
          messages.error(request, "Kode barang sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else:
          barang_supplier = BarangSupplier(
               kode_supplier = data_supplier,
               kode_barang = data_barang,
               quantity_satuan_small = quantity_satuan_small,
               quantity_satuan_medium = quantity_satuan_medium,
               quantity_satuan_large = quantity_satuan_large,
               satuan_harga_small = satuan_harga_small,
               satuan_harga_medium = satuan_harga_medium,
               satuan_harga_large = satuan_harga_large,
               timestamp = timestamp,
          ) 
          barang_supplier.save()  
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def update_barangsupplier(request,kode_supplier):
     barang_supplier = BarangSupplier.objects.select_related('kode_supplier','kode_barang').get(kode_supplier=kode_supplier)
     data_supplier = DataSupplier.objects.all().order_by('nama_supplier')
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     context = {
          'data_barangsupplier' : barang_supplier,
          'data_supplier' : data_supplier,
          'data_barang' : data_barang
     }
     return render(request, 'barangsupplier/u_barangsupplier.html',context)


def post_update_barangsupplier(request):
     kode_supplier = request.POST['kode_supplier']
     kode_barang = request.POST['kode_barang']
     quantity_satuan_small = request.POST['quantity_satuan_small']
     quantity_satuan_medium = request.POST['quantity_satuan_medium']
     quantity_satuan_large = request.POST['quantity_satuan_large']
     satuan_harga_small = request.POST['satuan_harga_small']
     satuan_harga_medium = request.POST['satuan_harga_medium']
     satuan_harga_large = request.POST['satuan_harga_large']
     timestamp = request.POST['timestamp']
     data_supplier, created = DataSupplier.objects.get_or_create(kode_supplier=kode_supplier)
     data_barang, created = DataBarang.objects.get_or_create(kode_barang=kode_barang)
     
     data_barangsupplier1 = BarangSupplier.objects.get(kode_supplier=data_supplier)
     data_barangsupplier1.kode_barang = data_barang
     data_barangsupplier1.quantity_satuan_small = quantity_satuan_small
     data_barangsupplier1.quantity_satuan_medium = quantity_satuan_medium
     data_barangsupplier1.quantity_satuan_large = quantity_satuan_large
     data_barangsupplier1.satuan_harga_small = satuan_harga_small
     data_barangsupplier1.satuan_harga_medium = satuan_harga_medium
     data_barangsupplier1.satuan_harga_large = satuan_harga_large
     data_barangsupplier1.timestamp = timestamp
     
     data_barangsupplier1.save()
     messages.success(request, 'Berhasil update data')
     return redirect('v_barangsupplier')

def delete_barangsupplier(request,kode_supplier):
     BarangSupplier.objects.get(kode_supplier=kode_supplier).delete()
     messages.success(request, 'Berhasil hapus data')

     return redirect('v_barangsupplier')

     # BarangSupplier

def v_transaksipembelian(request):
     data_transaksipembelian = TransaksiPembelian.objects.select_related('kode_supplier').all()
     context = {
          'data_transaksipembelian' : data_transaksipembelian
     }
     return render(request,'transaksipembelian/v_transaksipembelian.html',context)

def add_transaksipembelian(request):
     data_supplier = DataSupplier.objects.all().order_by('nama_supplier')
     data_barang = DataBarang.objects.all().order_by('nama_barang')
     data_hrgbarang = HargaBarang.objects.all().order_by('nama_barang')
     data_satuan = SatuanBarang.objects.all().order_by('nama_satuan')
     merged_data = []
     
     for barang, harga_barang in zip(data_barang, data_hrgbarang):
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
          'data_supplier' : data_supplier,
          'data_barang' : data_barang,
          'data_satuan' : data_satuan,
          'data_hrgbarang' : merged_data
     }
     return render(request, 'transaksipembelian/add_transaksipembelian.html',context)

def post_add_transaksipembelian(request):
     kode_transaksi_pembelian = request.POST['kode_transaksi_pembelian']
     kode_supplier = request.POST['kode_supplier']
     kode_barang_list = request.POST.getlist('kode_barang[]')
     kode_satuan_list = request.POST.getlist('nama_satuan[]')
     harga_pembelian_list = request.POST.getlist('harga_barang[]')
     quantity_list = request.POST.getlist('quantity_sales[]')
     ppn_barang_transaksi_list = request.POST.getlist('ppn_barang_transaksi[]')
     diskon_transaksi = request.POST['diskon_transaksi']
     biaya_pengiriman = request.POST['biaya_pengiriman']
     total_pembelian = request.POST['total_pembelian']
     jenis_pembayaran = request.POST['jenis_pembayaran']
     total_pembayaran = request.POST['total_pembayaran']
     tagihan_awal = request.POST['sisa_tagihan']
     sisa_tagihan = request.POST['sisa_tagihan']
     status = request.POST['status']
     timestamp = request.POST['timestamp']
     data_supplier, created = DataSupplier.objects.get_or_create(kode_supplier=kode_supplier)
     
     if TransaksiPembelian.objects.filter(kode_transaksi_pembelian=kode_transaksi_pembelian).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          with transaction.atomic():
            data_transaksipembelian = TransaksiPembelian(
               kode_transaksi_pembelian = kode_transaksi_pembelian,
               kode_supplier = data_supplier,
               biaya_pengiriman = biaya_pengiriman,
               diskon_transaksi = diskon_transaksi,
               total_pembelian = total_pembelian,
               jenis_pembayaran = jenis_pembayaran,
               total_pembayaran = total_pembayaran,
               tagihan_awal = tagihan_awal,
               sisa_tagihan = sisa_tagihan,
               status = status,
               timestamp = timestamp
            )
            data_transaksipembelian.save()
            for i in range(len(kode_barang_list)):
                data_barang, created = DataBarang.objects.get_or_create(kode_barang=kode_barang_list[i])
                DetailPembelian.objects.create(
                    kode_transaksi_pembelian=data_transaksipembelian,
                    kode_barang=data_barang,
                    nama_satuan=kode_satuan_list[i],
                    harga_total=harga_pembelian_list[i],
                    ppn_barang_transaksi=ppn_barang_transaksi_list[i],
                    quantity=quantity_list[i],
                )

                my_model_instances = StokBarang.objects.filter(kode_barang=kode_barang_list[i])
                for instance in my_model_instances:
                    quantity_sales = int(quantity_list[i])
                    instance.stok_satuan_small += quantity_sales
                    instance.save()
                    
     messages.success(request, 'Berhasil tambah data')
     return redirect('v_transaksipembelian')
     
def delete_transaksipembelian(request, kode_transaksi_pembelian):
     TransaksiPembelian.objects.get(kode_transaksi_pembelian=kode_transaksi_pembelian).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_transaksipembelian')

# Operasional

def v_operasional(request):
     data_operasional = Operasional.objects.all().order_by('kode_operasional')
     context = {
          'data_operasional' : data_operasional
     }
     return render(request,'operasional/v_operasional.html',context)

def post_add_operasional(request):
     kode_operasional = request.POST['kode_operasional']
     lokasi_awal = request.POST['lokasi_awal']
     lokasi_tujuan = request.POST['lokasi_tujuan']
     jenis_transportasi = request.POST['jenis_transportasi']
     timestamp = request.POST['timestamp']
     
     if Operasional.objects.filter(kode_operasional=kode_operasional).exists():
          messages.error(request, "Kode sudah ada!")
          return redirect(request.META.get('HTTP_REFERER','/'))
     else :
          data_operasioal = Operasional (
               kode_operasional = kode_operasional,
               lokasi_awal =lokasi_awal,
               lokasi_tujuan = lokasi_tujuan,
               jenis_transportasi = jenis_transportasi,
               timestamp = timestamp
          )
          data_operasioal.save()
          messages.success(request, 'Berhasil tambah data')
          return redirect(request.META.get('HTTP_REFERER','/'))
     
def delete_operasional(request,kode_operasional):
     data_operasional = Operasional.objects.get(kode_operasional=kode_operasional).delete()
     messages.success(request, 'Berhasil hapus data')
     return redirect('v_operasional')
#Lainnya
def hutang_piutang(request):
    data_hutang_piutang = SalesTransactions.objects.filter(sisa_tagihan__gt=0)
    data_customers = Customers.objects.all()

    context = {
        'data_hutang_piutang': data_hutang_piutang,
        'data_customers': data_customers
    }
    return render(request, 'laporan/hutang_piutang.html', context)

def hutang_to_supp(request):
     data_hutang = TransaksiPembelian.objects.filter(sisa_tagihan__gt=0)
     data_supplier = DataSupplier.objects.all()
     
     context ={
          'data_hutang' : data_hutang,
          'data_supplier' : data_supplier
     }
     return render(request,'laporan/hutang_to_supp.html',context)



def detail_transaksi(request, kode_sales):
    data_customer = SalesTransactions.objects.get(kode_sales=kode_sales)
    data_detailtransaksi = DetailTransaksi.objects.filter(kode_sales=kode_sales)
    data_retail = Retails.objects.all()
    
    
#     if data_detailtransaksi:
#         # Jika data_detailtransaksi tidak kosong, ambil data SalesTransactions dengan kode_sales yang sama
#         data_customers = SalesTransactions.objects.filter(kode_sales=kode_sales)
#     else:
#         data_customers = None

    context = {
        'data_detail': data_detailtransaksi,
        'data_customer': data_customer,
        'data_retail' : data_retail
    }

    return render(request, 'sales_transactions/detail_transaksi.html', context)



def detail_pembelian(request,kode_transaksi_pembelian):
     data_pembelian = TransaksiPembelian.objects.select_related('kode_supplier').get(kode_transaksi_pembelian=kode_transaksi_pembelian)
     data_detailpembelian = DetailPembelian.objects.filter(kode_transaksi_pembelian=kode_transaksi_pembelian)
     data_pengiriman = Pengiriman.objects.filter(kode_pengiriman=kode_transaksi_pembelian) 
     data_retail = Retails.objects.all()
     context = {
          'data_detail' : data_detailpembelian,
          'data_retail' : data_retail,
          'data_pembelian' : data_pembelian,
          'data_pengiriman' : data_pengiriman
     }
     return render(request, 'transaksipembelian/detail_pembelian.html',context)

def bayar_piutang(request,kode_sales):
     data_piutang = SalesTransactions.objects.get(kode_sales=kode_sales)
     context = {
          'data_piutang' :data_piutang
     }
     return render(request,'v_bayarpiutang.html',context)

def bayar_hutang(request,kode_transaksi_pembelian):
     data_hutang = TransaksiPembelian.objects.get(kode_transaksi_pembelian=kode_transaksi_pembelian)
     context = {
          'data_hutang' : data_hutang
     }
     return render(request,'v_bayarhutang.html',context)

def post_bayar_piutang(request):
    kode_sales = request.POST['kode_sales']
    bayar_tagihan = Decimal(request.POST['bayar_tagihan'])
    data_piutang = SalesTransactions.objects.get(kode_sales=kode_sales)
    
    # Tambahkan nilai ke total_pembayaran_sales
    data_piutang.total_pembayaran_sales += bayar_tagihan
    
    # Kurangkan nilai dari sisa_tagihan
    data_piutang.sisa_tagihan -= bayar_tagihan
    
    # Simpan perubahan ke database
    data_piutang.save()
    messages.success(request, 'Berhasil Bayar Piutang')
    return redirect('hutang_piutang')

def post_bayar_hutang(request):
     kode_transaksi_pembelian = request.POST['kode_transaksi_pembelian']
     bayar_hutang = Decimal(request.POST['bayar_hutang'])
     data_hutang = TransaksiPembelian.objects.get(kode_transaksi_pembelian=kode_transaksi_pembelian)
     
     data_hutang.total_pembayaran += bayar_hutang
     data_hutang.sisa_tagihan -= bayar_hutang
     data_hutang.save()
     messages.success(request, 'Berhasil Bayar Hutang')
     return redirect('hutang_to_supp')
     
     
     

def biaya_operasional(request,kode_transaksi_pembelian):
     data_transaksipembelian = TransaksiPembelian.objects.get(kode_transaksi_pembelian=kode_transaksi_pembelian)
     data_operasional = Operasional.objects.all().order_by('kode_operasional')
     data_pengiriman = Pengiriman.objects.all().order_by('kode_pengiriman')
     context = {
          'data_transaksipembelian' : data_transaksipembelian,
          'data_operasional' : data_operasional,
          'data_pengiriman' : data_pengiriman
     }
     return render(request,'biaya_operasional.html',context)

def post_biaya_operasional(request):
     kode_pengiriman = request.POST['kode_pengiriman']
     jalur_pengiriman = request.POST['jalur_pengiriman']
     biaya_pengiriman = request.POST['biaya_pengiriman']
     timestamp = request.POST['timestamp']
     
     data_pengiriman = Pengiriman (
               kode_pengiriman = kode_pengiriman,
               jalur_pengiriman =jalur_pengiriman,
               biaya_pengiriman = biaya_pengiriman,
               timestamp = timestamp
          )
     data_pengiriman.save()
     messages.success(request, 'Berhasil tambah data')
     return redirect(request.META.get('HTTP_REFERER','/'))
     

     



