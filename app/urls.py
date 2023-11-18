from django.urls import path
from .views import index, add_admins,post_add_admins

urlpatterns = [
    path('index',index,name='index'),
    path('add_admins',add_admins,name='add_admins'),
    path('post_add_admins',post_add_admins,name='post_add_admins')
]
