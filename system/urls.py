"""
URL configuration for system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from monitoring.views import overview,choro,reports,tables,download
#from monitoring.admin import custom_admin_site

urlpatterns = [
    path('admin/overview/', overview, name='overview'),
    path('admin/overview/choropleth_map/', choro, name='choro'),
    path('admin/overview/reports/', reports, name='reports'),
    path('admin/overview/tables/', tables, name='tables'),
    path('admin/overview/download/', download, name='download'),
    path('admin/', admin.site.urls),

    path('',include('monitoring.urls')),
    #path('admin/downloads/', custom_admin_site.admin_view(views.table), name='admin_downloads'),  # Custom admin downloads view
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


