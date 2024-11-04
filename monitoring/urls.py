from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.conf.urls.static import static
from .views import download_excel,export_excel,exp_excel,download_report_excel,download_report_pdf,download_masterlist_excel,download_masterlist_pdf,pdf_report_create
from .views import logout


app_name = 'monitoring'

urlpatterns = [
    path('',views.index,name='index'),
    path('add-logo/', views.add_logo, name='add_logo'),
    path('logos/', views.logo_list, name='logo_list'),
    path('choropleth_map/',views.choropleth_map,name='choropleth_map'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('admin/logout/', views.logout, name='logout'),
    #path('admin/downloads/', views.table, name='table'),
    path('overview/', views.overview, name='overview'),
    path('overview/choropleth_map/', views.choro, name='choro'),
    path('overview/reports/', views.reports, name='reports'),
    path('overview/tables/', views.tables, name='tables'),
    path('overview/download/', views.download, name='download'),
    path('overview/download_excel/', download_excel, name='download_excel'),
    path('overview/export_excel/', export_excel, name='export_excel'),
    path('overview/exp_excel/', exp_excel, name='exp_excel'),
    path('download_report_excel/', download_report_excel, name='download_report_excel'),
    path('download_report_pdf/', pdf_report_create, name='download_report_pdf'),
    path('download_masterlist_excel/', download_masterlist_excel, name='download_masterlist_excel'),
    path('download_masterlist_pdf/', download_masterlist_pdf, name='download_masterlist_pdf'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

