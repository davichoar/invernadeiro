from app.models import Usuario, Auditoria
from app.permissions import *
from django.shortcuts import render
import json

def veraudit(request, template='app/auditoria/logAuditoria.html'):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Auditoria"):
            return accesodenegado(request)
        listaAuditoria = Auditoria.objects.all()
        if listaAuditoria is not None:
            listaAuditoria = listaAuditoria.order_by('-fecha')
        usuariosTodos = Usuario.objects.all()
        listaUsuarios = dict()
        for usuario in usuariosTodos:
            listaUsuarios[usuario.idusuario] = usuario
        context = { 
            'listaUsuarios': listaUsuarios,
            'listaAuditoria': listaAuditoria,
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero')
        }
        return render(request, template, context)

def detalleaudit(request, idAuditoria, template='app/auditoria/detalleAuditoria.html'):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Auditoria"):
            return accesodenegado(request)
        auditoria = Auditoria.objects.get(idauditoria=idAuditoria)
        dataNueva  = json.loads(auditoria.datanueva)
        listaLlaves = list(dataNueva.keys())
        if auditoria.dataantigua != '':
            dataAntigua  = json.loads(auditoria.dataantigua)
            llavesQuitar = []
            for llave in listaLlaves:
                if dataAntigua[llave] == dataNueva[llave]:
                    llavesQuitar.append(llave)
            for llaveQuitar in llavesQuitar:
                listaLlaves.remove(llaveQuitar)
            if 'idusuarioauditado' in listaLlaves:
                listaLlaves.remove('idusuarioauditado')
        else:
            dataAntigua = dict()
            for llave in listaLlaves:
                dataAntigua[llave] = ''
        context = { 
            'listaLlaves': listaLlaves,
            'dataAntigua': dataAntigua,
            'dataNueva': dataNueva,
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero')
        }
        return render(request, template, context)
        
        