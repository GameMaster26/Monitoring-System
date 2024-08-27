from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin


app_name = 'monitoring'

urlpatterns = [
    path('',views.index,name='index'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('admin/logout/', admin.site.logout, name='logout'),
    #path('admin/downloads/', views.table, name='table'),
    path('monitor/download/', views.table, name='table'),
    path('download/pdf/', views.download_pdf, name='download_pdf'),
    path('download/excel/', views.download_excel, name='download_excel'),
    path('admin/', views.notification, name='notification'),
    path('admin/notifications/',views.notification, name='notification'),
]