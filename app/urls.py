from django.urls import path
from .views import *


urlpatterns = [
    
    #Login
    path('superadmin_login',superadmin_login,name='superadmin_login'),
    path('post_superadmin_login',post_superadmin_login,name='post_superadmin_login'),
    path('logout',logout,name='logout'),
    
    #Dashboard
    
    path('dashboard',dashboard,name='dashboard'),
    
    # Admins
    
    path('v_admins',v_admins,name='v_admins'),
    path('add_admins',add_admins,name='add_admins'),
    path('post_add_admins',post_add_admins,name='post_add_admins'),
    path('update_admins/<str:kode_admin>',update_admins,name='update_admins'),
    path('post_update_admins',post_update_admins,name='post_update_admins'),
    path('delete_admins/<str:kode_admin>',delete_admins,name='delete_admins'),
    
    # SatuanBarang
    
    path('v_satuanbarang',v_satuanbarang,name='v_satuanbarang'),
    path('add_satuanbarang',add_satuanbarang,name='add_satuanbarang'),
    path('post_add_satuanbarang',post_add_satuanbarang,name='post_add_satuanbarang'),
    path('update_satuanbarang/<str:kode_satuan>',update_satuanbarang,name='update_satuanbarang'),
    path('post_update_satuanbarang',post_update_satuanbarang,name='post_update_satuanbarang'),
    path('delete_satuanbarang/<str:kode_satuan>',delete_satuanbarang,name='delete_satuanbarang'),
    
    # KelompokBarang
    
    path('v_kelompokbarang',v_kelompokbarang,name='v_kelompokbarang'),
    path('add_kelompokbarang',add_kelompokbarang,name='add_kelompokbarang'),
    path('post_add_kelompokbarang',post_add_kelompokbarang,name='post_add_kelompokbarang'),
    path('update_kelompokbarang/<str:kode_kelompok>',update_kelompokbarang,name='update_kelompokbarang'),
    path('post_update_kelompokbarang',post_update_kelompokbarang,name='post_update_kelompokbarang'),
    path('delete_kelompokbarang/<str:kode_kelompok>',delete_kelompokbarang,name='delete_kelompokbarang'),
    
    # Gudang
    
    path('v_gudang',v_gudang,name='v_gudang'),
    path('add_gudang',add_gudang,name='add_gudang'),
    path('post_add_gudang',post_add_gudang,name='post_add_gudang'),
    path('update_gudang/<str:kode_gudang>',update_gudang,name='update_gudang'),
    path('post_update_gudang',post_update_gudang,name='post_update_gudang'),
    path('delete_gudang<str:kode_gudang>',delete_gudang,name='delete_gudang'),

    # JenisBarang
    
    path('v_jenisbarang',v_jenisbarang,name='v_jenisbarang'),
    path('add_jenisbarang',add_jenisbarang,name='add_jenisbarang'),
    path('post_add_jenisbarang',post_add_jenisbarang,name='post_add_jenisbarang'),
    path('update_jenisbarang/<str:kode_jenis>',update_jenisbarang,name='update_jenisbarang'),
    path('post_update_jenisbarang',post_update_jenisbarang,name='post_update_jenisbarang'),
    path('delete_jenisbarang/<str:kode_jenis>',delete_jenisbarang,name='delete_jenisbarang'),
    
    # DataBarang
    
    path('v_databarang',v_databarang,name='v_databarang'),
    path('add_databarang',add_databarang,name='add_databarang'),
    path('post_add_databarang',post_add_databarang,name='post_add_databarang'),
    path('update_databarang<str:kode_barang>',update_databarang,name='update_databarang'),
    path('post_update_databarang',post_update_databarang,name='post_update_databarang'),
    path('delete_databarang/<str:kode_barang>',delete_databarang,name='delete_databarang'),
    
    # StokBarang
    
    path('v_stokbarang',v_stokbarang,name='v_stokbarang'),
    path('add_stokbarang',add_stokbarang,name='add_stokbarang'),
    path('post_add_stokbarang',post_add_stokbarang,name='post_add_stokbarang'),
    path('update_stokbarang/<str:kode_stok>',update_stokbarang,name='update_stokbarang'),
    path('post_update_stokbarang',post_update_stokbarang,name='post_update_stokbarang'),
    path('delete_stokbarang/<str:kode_stok>',delete_stokbarang,name='delete_stokbarang'),
    
    # HargaBarang
    
    path('v_hargabarang',v_hargabarang,name='v_hargabarang'),
    path('add_hargabarang',add_hargabarang,name='add_hargabarang'),
    path('post_add_hargabarang',post_add_hargabarang,name='post_add_hargabarang'),
    path('update_hargabarang/<str:kode_harga>',update_hargabarang,name='update_hargabarang'),
    path('post_update_hargabarang',post_update_hargabarang,name='post_update_hargabarang'),
    path('delete_hargabarang/<str:kode_harga>',delete_hargabarang,name='delete_hargabarang'),
    
    # JenisCustomers
    
    path('v_jeniscustomers',v_jeniscustomers,name='v_jeniscustomers'),
    path('add_jeniscustomers',add_jeniscustomers,name='add_jeniscustomers'),
    path('post_add_jeniscustomer',post_add_jeniscustomer,name='post_add_jeniscustomer'),
    path('update_jeniscustomers/<str:kode_jenis_customers>',update_jeniscustomers,name='update_jeniscustomers'),
    path('post_update_jeniscustomers',post_update_jeniscustomers,name='post_update_jeniscustomers'),
    path('delete_jeniscustomers/<str:kode_jenis_customers>',delete_jeniscustomers,name='delete_jeniscustomers'),
    
    # Customers
    
    path('v_customers',v_customers,name='v_customers'),
    path('post_add_customers',post_add_customers,name='post_add_customers'),
    path('update_customers/<str:kode_customers>',update_customers,name='update_customers'),
    path('post_update_customers',post_update_customers,name='post_update_customers'),
    path('delete_customers/<str:kode_customers>',delete_customers,name='delete_customers'),
    
    # Sopir
    
    path('v_sopir',v_sopir,name='v_sopir'),
    path('post_add_sopir',post_add_sopir,name='post_add_sopir'),
    path('update_sopir/<str:kode_sopir>',update_sopir,name='update_sopir'),
    path('post_update_sopir',post_update_sopir,name='post_update_sopir'),
    path('delete_sopir/<str:kode_sopir>',delete_sopir,name='delete_sopir'),
    
    # SalesTransactions
    
    path('v_salestransactions',v_salestransactions,name='v_salestransactions'),
    path('add_salestransactions',add_salestransactions,name='add_salestransactions'),
    path('post_add_salestransactions',post_add_salestransactions,name='post_add_salestransactions'),
    
    # DataSupplier
    path('v_datasupplier',v_datasupplier,name='v_datasupplier'),
    path('add_datasupplier',add_datasupplier,name='add_datasupplier'),
    path('post_add_datasupplier',post_add_datasupplier,name='post_add_datasupplier'),
    path('update_datasupplier<str:kode_supplier>',update_datasupplier,name='update_datasupplier'),
    path('post_update_datasupplier',post_update_datasupplier,name='post_update_datasupplier'),
    path('delete_datasupplier<str:kode_supplier>',delete_datasupplier,name='delete_datasupplier'),
    
    #BarangSupllier
    path('v_barangsupplier',v_barangsupplier,name='v_barangsupplier'),

]
