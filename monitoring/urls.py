from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.conf.urls.static import static


app_name = 'monitoring'

urlpatterns = [
    path('',views.index,name='index'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('admin/logout/', admin.site.logout, name='logout'),
    #path('admin/downloads/', views.table, name='table'),
    path('reports/', views.overview, name='overview'),
    path('reports/reports/', views.reports, name='reports'),
    path('reports/tables/', views.tables, name='tables'),
    path('reports/download/', views.download, name='download'),
    path('admin/', views.notification, name='notification'),
    path('admin/notifications/',views.notification, name='notification'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

