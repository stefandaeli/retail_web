from django.urls import path
from .views import dashboard, v_admins, add_admins,post_add_admins, update_admins, post_update_admins, delete_admins

urlpatterns = [
    path('dashboard',dashboard,name='dashboard'),
    # Admins
    path('v_admins',v_admins,name='v_admins'),
    path('add_admins',add_admins,name='add_admins'),
    path('post_add_admins',post_add_admins,name='post_add_admins'),
    path('update_admins/<str:kode_admin>',update_admins,name='update_admins'),
    path('post_update_admins',post_update_admins,name='post_update_admins'),
    path('delete_admins/<str:kode_admin>',delete_admins,name='delete_admins')
    
]
