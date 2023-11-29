from django.db import models

#Admins
class Admins(models.Model):
    kode_admin = models.CharField(max_length=20,primary_key=True)
    nama_admin = models.CharField(max_length=50)
    password_admin = models.CharField(max_length=20)
    timestamp = models.DateTimeField(null=True)
    
    
#Barang
class SatuanBarang(models.Model):
    kode_satuan = models.CharField(max_length=20,primary_key=True)
    nama_satuan = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)

class KelompokBarang(models.Model):
    kode_kelompok = models.CharField(max_length=20,primary_key=True)
    nama_kelompok = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)

class Gudang(models.Model):
    kode_gudang = models.CharField(max_length=20,primary_key=True)
    nama_gudang = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)
    
class JenisBarang(models.Model):
    kode_jenis = models.CharField(max_length=20,primary_key=True)
    nama_jenis = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)
    
class DataBarang(models.Model):
    kode_barang = models.CharField(max_length=20,primary_key=True)
    nama_barang = models.CharField(max_length=200)
    kelompok_barang =models.CharField(max_length=50)
    jenis_barang = models.CharField(max_length=50)
    satuan_barang_small = models.CharField(max_length=50)
    satuan_barang_medium = models.CharField(max_length=50)
    satuan_barang_large = models.CharField(max_length=50)
    tgl_expire_barang = models.DateField(null=True)
    timestamp = models.DateTimeField(null=True)


    
