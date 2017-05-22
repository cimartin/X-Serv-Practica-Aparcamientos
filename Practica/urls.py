"""Practica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import logout, login
from django.views.static import serve
from django.views.generic import RedirectView
from aparcamientos import views as aparcamientos_views

urlpatterns = [
    url(r'^$', aparcamientos_views.homepage, name='homepage'),
    url(r'^aparcamientos$', aparcamientos_views.aparcamientos, name="aparcamientos"),
    url(r'^aparcamientos/(\d+)', aparcamientos_views.aparcamiento_info, name='aparcamiento_info'),
    url(r'^about$', aparcamientos_views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', aparcamientos_views.registro, name='registro'),
    url(r'^login/$', aparcamientos_views.autenticacion, name='autenticacion'),
    url(r'^aparcamientos/login/$', aparcamientos_views.autenticacion, name='autenticacion'),
    url(r'^logout/$', logout, name="logout"),
    url(r'^aparcamientos/logout/$', logout, name='logout'),
    url(r'^(.*)/xml$', aparcamientos_views.user_xml, name='user_xml'),
    url(r'^css/style.css$', aparcamientos_views.css, name="css"),
    url(r'^aparcamientos/css/style.css$', aparcamientos_views.css, name='css'),
    url(r'^aparcamientos/js/(.*)$', serve, {'document_root' : 'templates/template_html/js'}, name='js'),
    url(r'^aparcamientos/images/(.*)$', serve, {'document_root' : 'templates/template_html/images'}, name='images'),
    url(r'^aparcamientos/fonts/(.*)$', serve, {'document_root' : 'templates/template_html/fonts'}, name='fonts'),
    url(r'^js/(.*)$', serve, {'document_root': 'templates/template_html/js'}, name = "js"),
    url(r'^images/(.*)$', serve, {'document_root': 'templates/template_html/images'}, name='images'),
    url(r'^fonts/(.*)$', serve, {'document_root' : 'templates/template_html/fonts'}, name="fonts"),
    url(r'^(.*)$', aparcamientos_views.userpage, name='userpage'),
]
