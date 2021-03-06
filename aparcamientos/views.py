# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from aparcamientos.models import Aparcamientos, Configuracion, Comentarios, Seleccionados
from dataBase import create_dataBase
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.template import loader
import itertools
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import time

# Create your views here.

def homepage(request):
    aparcamientos = Aparcamientos.objects.all()
    tds_config = Configuracion.objects.all()
    if(not aparcamientos):
        names, addresses, districs, neighs, urls, descriptions, accessibilities, phones, mails, lats, longs = create_dataBase()
        for nombre, direccion, distrito, barrio, url, descripcion, accesibilidad, telef, mail, lat, longt in zip(names, addresses, districs, neighs, urls, descriptions, accessibilities, phones, mails, lats, longs):
            nuevo_parc = Aparcamientos(nombre=nombre, direccion=direccion, distrito=distrito, barrio=barrio, url=url, descripcion=descripcion,
                        accesibilidad=accesibilidad, telefono=telef, mail=mail, latitud=lat, longitud=longt)
            nuevo_parc.save()

    aparcamientos_comentados = Comentarios.objects.all().values()
    ids = []
    ids_aux = []
    for aparcamiento in aparcamientos_comentados:
        ids.append(aparcamiento['aparcamiento_comentado_id'])
    for id_aux in ids:
        if not id_aux in ids_aux:
            ids_aux.append(id_aux)
    parcs = []
    for id_n in ids_aux:
        parcs.append(Aparcamientos.objects.filter(id=id_n))
    parcs_aux = []
    for parc in parcs:
        parcs_aux.append(parc[0])

    if(request.method == "GET"):
        template = get_template('index.html')
        context = RequestContext(request, {'parcs_aux' : parcs_aux, 'tds_config' : tds_config})
        return HttpResponse(template.render(context))

    if(request.method == "POST"):
        accesibles = request.POST.get('accesibles')
        hidden = request.POST.get('activado')
        if(accesibles != None and hidden == "on"):
            titulo = "Listado accesibles : "
            aparcamientos_accs = Aparcamientos.objects.filter(accesibilidad=1)
            template = loader.get_template('index.html')
            context = {'aparcamientos_accs' : aparcamientos_accs, 'tds_config' : tds_config, 'titulo' : titulo}
            return(HttpResponse(template.render(context, request)))
        elif(accesibles != None and hidden == "off"):
            titulo = "Todos : "
            aparcamientos_accs = aparcamientos
            template = loader.get_template('index.html')
            context = {'aparcamientos_accs' : aparcamientos_accs, 'tds_config' : tds_config, 'titulo' : titulo}
            return(HttpResponse(template.render(context, request)))
        else:
            favs = []
            favs = parcs_aux
            context = {"favs" : favs}
            template = get_template("userXML.xml")
            return(HttpResponse(template.render(context, request), content_type="text/xml"))

@csrf_exempt
def userpage(request, user):
    tds_config = Configuracion.objects.all()
    user_act = User.objects.get(username=user)
    favs = Seleccionados.objects.filter(usuario=user_act)
    user_config = Configuracion.objects.get(usuario=user_act)
    seleccionados = []
    fechas = []
    auxs = []
    for fav in favs:
        seleccionados.append(fav.aparcamiento_seleccionado)
        fechas.append(fav.fecha)
    auxs = zip(seleccionados, fechas)
    if(request.method == "POST"):
        titulo_nuevo = request.POST.get("newTitle")
        nuevo_BG = request.POST.get("backgroundSelected")
        nuevo_tamano = request.POST.get("letterSize")
        user = User.objects.get(username=user)
        nueva_config = Configuracion.objects.get(usuario=user)
        if(titulo_nuevo != "Titulo de la pagina." and titulo_nuevo != nueva_config.titulo and titulo_nuevo != None):
            print(titulo_nuevo)
            nueva_config.titulo = titulo_nuevo
            nueva_config.save()
        if(nuevo_BG != None and nuevo_BG != nueva_config.bg_color):
            nueva_config.bg_color = nuevo_BG
            nueva_config.save()
        if(nuevo_tamano != None and nuevo_tamano != nueva_config.tamano_ltr):
            nueva_config.tamano_ltr = nuevo_tamano
            nueva_config.save()

    context = {'auxs' : auxs, 'user_config' : user_config, 'user_act' : user_act, 'tds_config' : tds_config}
    template = loader.get_template('pagina_usuario.html')
    return(HttpResponse(template.render(context, request)))

@csrf_exempt
def aparcamientos(request):
    tds_config = Configuracion.objects.all()
    distritos = []
    aparcamientos = Aparcamientos.objects.all()
    for aparcamiento in aparcamientos:
        distritos.append(getattr(aparcamiento, 'distrito'))
    distritos_aux = []
    for distrito in distritos:
        if not distrito in distritos_aux:
            distritos_aux.append(distrito)
    if(request.method == "POST"):
        distrito = request.POST.get('distrito')
        if(distrito != None):
            aparcamientos = Aparcamientos.objects.filter(distrito=distrito)
        else:
            aparcamientos = Aparcamientos.objects.all()

    template = loader.get_template('aparcamientos.html')
    context = {'aparcamientos' : aparcamientos, 'distritos_aux': distritos_aux, 'tds_config' : tds_config}
    return(HttpResponse(template.render(context, request)))

def aparcamiento_info(request, id):
    aparcamiento = Aparcamientos.objects.get(id=id)
    comentarios = Comentarios.objects.filter(aparcamiento_comentado=aparcamiento)
    tds_config = Configuracion.objects.all()

    if(request.method == "POST"):
        fav = request.POST.get('aparcamiento')
        comentario = request.POST.get('comentario')
        if(comentario != None and comentario != "Escribe tu comentario."):
            user = User.objects.get(username=request.user.username)
            nuevo_coment = Comentarios(texto=comentario, autor=user, aparcamiento_comentado=aparcamiento)
            nuevo_coment.save()
        if(fav != None):
            user = User.objects.get(username=request.user.username)
            fecha = time.strftime("%d/%m/%y")
            nuevo_fav = Seleccionados(aparcamiento_seleccionado=aparcamiento, usuario=user, fecha=fecha)
            nuevo_fav.save()

    template = get_template('aparcamiento.html')
    context = RequestContext(request, {'aparcamiento' : aparcamiento, 'comentarios' : comentarios, 'tds_config' : tds_config})
    return HttpResponse(template.render(context))

def user_xml(request, user_xml):
    user = User.objects.get(username=user_xml)
    seleccs = Seleccionados.objects.filter(usuario=user)
    favs = []
    for selecc in seleccs:
        favs.append(selecc.aparcamiento_seleccionado)
    context = {"favs" : favs}
    template = get_template("userXML.xml")
    return (HttpResponse(template.render(context, request), content_type='application/xhtml+xml'))

@csrf_exempt
def autenticacion(request):
    if(request.method == "POST"):
        username = request.POST.get('login')
    password = request.POST.get('password')
    users = User.objects.all()
    user = authenticate(username=username, password=password)
    if(user is not None):
        login(request, user)
    return HttpResponseRedirect("/")

@csrf_exempt
def registro(request):
    if(request.method == "POST"):
        nickname = request.POST.get("login")
        passwd = make_password(request.POST.get("password"))
        nuevo_usuario = User(username=nickname, password=passwd)
        nuevo_usuario.save()
        user = User.objects.get(username=nickname)
        nueva_configuracion = Configuracion(usuario=user)
        nueva_configuracion.save()
    return HttpResponseRedirect("/")

def css(request):
    color_bg = "blue"
    tamano = 12
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        user_config = Configuracion.objects.get(usuario=user)
        color_bg = user_config.bg_color
        tamano = user_config.tamano_ltr
    template = get_template("css/style.css")
    context ={"color_bg": color_bg, "tamano": tamano}
    return (HttpResponse(template.render(context, request), content_type="text/css"))

def about(request):
    template = get_template('about.html')
    return HttpResponse(template.render())
