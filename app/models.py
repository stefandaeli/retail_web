from django.db import models

#SuperAdmins

class SuperAdmins(models.Model):
    kode_superadmin = models.CharField(max_length=20,primary_key=True)
    nama_superadmin = models.CharField(max_length=120)
    password_superadmin = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)

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

class StokBarang(models.Model):
   kode_stok = models.CharField(max_length=20, primary_key=True)
   kode_barang = models.CharField(max_length=20,null=True)
   nama_barang = models.CharField(max_length=120, null=True)
   stok_satuan_small = models.CharField(max_length=20)
   stok_satuan_medium = models.CharField(max_length=20)
   stok_satuan_large = models.CharField(max_length=20)
   nama_gudang = models.CharField(max_length=50)
   timestamp = models.DateTimeField(null=True)
    
class HargaBarang(models.Model):
    kode_harga = models.CharField(max_length=20,primary_key=True)
    kode_barang = models.CharField(max_length=20,null=True)
    nama_barang = models.CharField(max_length=120)
    harga_satuan_small = models.IntegerField()
    harga_satuan_medium = models.IntegerField()
    harga_satuan_large = models.IntegerField()
    ppn_barang = models.IntegerField(null=True)
    diskon_barang = models.IntegerField()
    timestamp = models.DateTimeField(null=True)
    
class JenisCustomers(models.Model):
    kode_jenis_customers = models.CharField(max_length=20,primary_key=True)
    nama_jenis_customers = models.CharField(max_length=120)
    timestamp = models.DateTimeField(null=True)
    
class Customers(models.Model):
    kode_customers = models.CharField(max_length=20,primary_key=True)
    nama_customers = models.CharField(max_length=120)
    jenis_customers = models.CharField(max_length=120)
    alamat_customers = models.CharField(max_length=120,null=True)
    wa_customer = models.CharField(max_length=20,null=True)
    email_customers = models.CharField(max_length=120,null=True)
    timestamp = models.DateTimeField(null=True)
    
class Sopir(models.Model):
    kode_sopir = models.CharField(max_length=20,primary_key=True)
    nama_sopir = models.CharField(max_length=120)
    alamat_sopir = models.CharField(max_length=120)
    wa_sopir = models.CharField(max_length=20)
    email_sopir = models.CharField(max_length=120,null=True)
    timestamp = models.DateTimeField(null=True)
    
class SalesTransactions(models.Model):
    kode_sales = models.CharField(max_length=120,primary_key=True)
    nama_customers = models.CharField(max_length=120,null=True)
    kode_customers = models.CharField(max_length=20,null=True)
    nama_sopir = models.CharField(max_length=120,null=True)
    kode_sopir = models.CharField(max_length=20,null=True)
    nama_barang = models.CharField(max_length=120,null=True)
    kode_barang = models.CharField(max_length=20,null=True)
    nama_satuan = models.CharField(max_length=120,null=True)
    harga_barang = models.IntegerField(null=True)
    quantity_sales = models.IntegerField(null=True)
    diskon_sales = models.IntegerField(null=True)
    biaya_pengiriman = models.IntegerField(null=True)
    sub_total_sales = models.IntegerField(null=True)
    grand_total_sales = models.IntegerField(null=True)
    jenis_pembayaran = models.CharField(max_length=120,null=True)
    total_pembayaran_sales = models.IntegerField(null=True)
    sisa_tagihan = models.IntegerField(null=True)
    status = models.CharField(max_length=120,null=True)
    timestamp = models.DateTimeField(null=True)
    
#Supplier

class DataSupplier(models.Model):
    kode_supplier = models.CharField(max_length=120,primary_key=True)
    nama_supplier = models.CharField(max_length=120,null=True)
    alamat_supplier = models.CharField(max_length=120,null=True)
    npwp_supplier = models.CharField(max_length=50,null=True)
    tlp_supplier = models.CharField(max_length=13,null=True)
    email_supplier = models.CharField(max_length=120,null=True)
    wa_supplier = models.CharField(max_length=13,null=True)
    nama_bank_supplier = models.CharField(max_length=20,null=True)
    no_rek_supplier = models.CharField(max_length=20,null=True)
    ket_supplier = models.CharField(max_length=250,null=True)
    status_aktif_supplier = models.CharField(max_length=120,null=True)
    timestamp = models.DateTimeField(null=True)
    

    
    
    
    




    