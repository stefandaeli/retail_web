from django.urls import path
from .views import dashboard, v_admins, add_admins,post_add_admins, update_admins, post_update_admins, delete_admins
from .views import v_satuanbarang, add_satuanbarang, post_add_satuanbarang, update_satuanbarang, post_update_satuanbarang, delete_satuanbarang

urlpatterns = [
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
    path('delete_satuanbarang/<str:kode_satuan>',delete_satuanbarang,name='delete_satuanbarang')
    
]
