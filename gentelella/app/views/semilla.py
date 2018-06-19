from django.shortcuts import render, redirect
from app.models import Tipoplanta, Semilla, Historiasemilla, Modulosemilla, Zona
from django.db.models import Max
from datetime import datetime
from django.db import transaction
from app.permissions import *

def casillaOcupada(idmodulo, posx, posy, semilla = None):
    if semilla is not None:
        semillasModulo = Semilla.objects.filter(idmodulo = idmodulo, habilitado = True).exclude(idsemilla=semilla.idsemilla)        
    else:
        semillasModulo = Semilla.objects.filter(idmodulo = idmodulo, habilitado = True)
    for semilla in semillasModulo:
        historiaSemilla = Historiasemilla.objects.filter(idsemilla=semilla.idsemilla).order_by('-fecharegistro')[0]
        if (int(historiaSemilla.posx) == int(posx) and int(historiaSemilla.posy) == int(posy)):
            return True
    return False

def getListaModulos(request):
    idInvernadero = request.session['idInvernadero']
    zonasInvernadero = Zona.objects.filter(idinvernadero = idInvernadero, habilitado=True)
    listaModulos = []
    for zona in zonasInvernadero:
        modulosZona = Modulosemilla.objects.filter(idzona = zona.idzona, habilitado=True)
        for modulo in modulosZona:
            listaModulos.append(modulo)
    return listaModulos
    
def crearFakes(request, idSemilla = -1):
    semillaFake = Semilla()
    semillaFake.idsemilla = idSemilla
    semillaFake.idmodulo = request.POST.get('modulo')
    semillaFake.idtipoplanta = int(request.POST.get('tipoPlanta'))
    historiaFake = Historiasemilla()
    historiaFake.idsemilla = idSemilla
    historiaFake.posx = request.POST.get('posx')
    historiaFake.posy = request.POST.get('posy')
    return semillaFake, historiaFake
    
def crear(request, idModulo, columna, fila, template='app/semilla/crearSemilla.html', extra_context=None):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Semilla"):
            return accesodenegado(request)
        listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
        semillaFake = Semilla()
        semillaFake.idtipoplanta = -1
        semillaFake.idmodulo = idModulo
        historiaFake = Historiasemilla()
        historiaFake.posx = columna
        historiaFake.posy = fila
        listaModulos = getListaModulos(request)
        context = {
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'semilla': semillaFake,
            'listaTipoplanta': listaTipoplanta,
            'listaModulos': listaModulos,
            'historia': historiaFake,
            'modulo': Modulosemilla.objects.get(idmodulo=idModulo),
            'idModuloOrig': idModulo
        }
        return render(request, template, context)
    elif request.method == 'POST':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Semilla"):
            return accesodenegado(request)
        nuevoid = Semilla.objects.all().aggregate(Max('idsemilla'))['idsemilla__max']
        if nuevoid is None:
            nuevoid = 1
        else:
            nuevoid += 1
        if (casillaOcupada(request.POST.get('modulo'), request.POST.get('posx'), request.POST.get('posy'))):
            listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
            listaModulos = getListaModulos(request)
            semillaFake, historiaFake = crearFakes(request)
            print(semillaFake.idmodulo)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'semilla': semillaFake,
                'listaTipoplanta': listaTipoplanta,
                'listaModulos': listaModulos,
                'historia': historiaFake,
                'modulo': Modulosemilla.objects.get(idmodulo=request.POST.get('modulo')),
                'mensajeError': 'El lugar donde está intentando colocar la semilla ya está en uso.',
                'idModuloOrig': idModulo
            }
            return render(request, template, context)
        try:
            with transaction.atomic():
                nuevaSemilla = Semilla.objects.create(
                    idsemilla = nuevoid,
                    idtipoplanta = request.POST.get('tipoPlanta'),
                    idmodulo = request.POST.get('modulo'),
                    fechacreacion = datetime.now(),
                    idusuarioauditado = request.session['idUsuarioActual'],
                    habilitado = True
                )
                nuevoidhistoria = Historiasemilla.objects.all().aggregate(Max('idhistoriasemilla'))['idhistoriasemilla__max']
                if nuevoidhistoria is None:
                    nuevoidhistoria = 1
                else:
                    nuevoidhistoria += 1
                nuevaHistoria = Historiasemilla.objects.create(
                    idhistoriasemilla = nuevoidhistoria,
                    idsemilla = nuevoid,
                    idmodulo = request.POST.get('modulo'),
                    posx = request.POST.get('posx'),
                    posy = request.POST.get('posy'),
                    fecharegistro = datetime.now()
                )
        except Exception as e:
            print(e)
            listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
            listaModulos = getListaModulos(request)
            semillaFake, historiaFake = crearFakes(request)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'semilla': semillaFake,
                'listaTipoplanta': listaTipoplanta,
                'listaModulos': listaModulos,
                'historia': historiaFake,
                'modulo': Modulosemilla.objects.get(idmodulo=request.POST.get('modulo')),
                'mensajeError': 'No se puede crear la semilla en este momento.',
                'idModuloOrig': idModulo
            }
            return render(request, template, context)
        request.session['mensajeSemillaCrear'] = True
        return redirect('moduloSemillaDetalle', request.POST.get('modulo'))
        
def detalle(request, idModulo, idSemilla, template='app/semilla/verEditarSemilla.html', extra_context=None):
    semilla = Semilla.objects.get(idsemilla = idSemilla)
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Semilla"):
            return accesodenegado(request)
        mostrarModalEditar = request.session.pop('mensajeSemillaEditar', False)
        listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
        listaModulos = getListaModulos(request)
        context = {
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'semilla': semilla,
            'listaTipoplanta': listaTipoplanta,
            'listaModulos': listaModulos,
            'historia': Historiasemilla.objects.filter(idsemilla=semilla.idsemilla).order_by('-fecharegistro')[0],
            'modulo': Modulosemilla.objects.get(idmodulo=semilla.idmodulo),
            'idModuloOrig': idModulo,
            'mostrarModalEditar': mostrarModalEditar,
            'editable': False
        }
        return render(request, template, context)
    if request.method == 'POST':
        if 'b_editar' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Semilla"):
                return accesodenegado(request)
            listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
            listaModulos = getListaModulos(request)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'semilla': semilla,
                'listaTipoplanta': listaTipoplanta,
                'listaModulos': listaModulos,
                'historia': Historiasemilla.objects.filter(idsemilla=semilla.idsemilla).order_by('-fecharegistro')[0],
                'modulo': Modulosemilla.objects.get(idmodulo=semilla.idmodulo),
                'idModuloOrig': idModulo,
                'editable': True
            }
            return render(request, template, context)
        if 'b_aceptar_modal' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Eliminar Semilla"):
                return accesodenegado(request)
            try:
                Semilla.objects.filter(idsemilla = idSemilla).update(habilitado=False, idusuarioauditado=request.session['idUsuarioActual'])
                request.session['mensajeSemillaEliminar'] = True
            except Exception as e:
                print(e)
            return redirect('moduloSemillaDetalle', idModulo)
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Editar Semilla"):
            return accesodenegado(request)
        if (casillaOcupada(request.POST.get('modulo'), request.POST.get('posx'), request.POST.get('posy'), semilla)):
            listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
            listaModulos = getListaModulos(request)
            semillaFake, historiaFake = crearFakes(request, semilla.idsemilla)
            print(semillaFake.idmodulo)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'semilla': semillaFake,
                'listaTipoplanta': listaTipoplanta,
                'listaModulos': listaModulos,
                'historia': historiaFake,
                'modulo': Modulosemilla.objects.get(idmodulo=request.POST.get('modulo')),
                'mensajeError': 'El lugar donde está intentando colocar la semilla ya está en uso.',
                'idModuloOrig': idModulo,
                'editable': True
            }
            return render(request, template, context)
        try:
            with transaction.atomic():
                Semilla.objects.filter(idsemilla=idSemilla).update(
                    idtipoplanta = request.POST.get('tipoPlanta'),
                    idmodulo = request.POST.get('modulo'),
                    fechacreacion = datetime.now(),
                    idusuarioauditado = request.session['idUsuarioActual'],
                    habilitado = True
                )
                
                nuevoidhistoria = Historiasemilla.objects.all().aggregate(Max('idhistoriasemilla'))['idhistoriasemilla__max']
                if nuevoidhistoria is None:
                    nuevoidhistoria = 1
                else:
                    nuevoidhistoria += 1
                nuevaHistoria = Historiasemilla.objects.create(
                    idhistoriasemilla = nuevoidhistoria,
                    idsemilla = semilla.idsemilla,
                    idmodulo = request.POST.get('modulo'),
                    posx = request.POST.get('posx'),
                    posy = request.POST.get('posy'),
                    fecharegistro = datetime.now()
                )
        except Exception as e:
            print(e)
            listaTipoplanta = Tipoplanta.objects.filter(habilitado = True)
            listaModulos = getListaModulos(request)
            semillaFake, historiaFake = crearFakes(request, semilla.idsemilla)            
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'semilla': semillaFake,
                'listaTipoplanta': listaTipoplanta,
                'listaModulos': listaModulos,
                'historia': historiaFake,
                'modulo': Modulosemilla.objects.get(idmodulo=request.POST.get('modulo')),
                'mensajeError': 'Error en la edición de semilla.',
                'idModuloOrig': idModulo,
                'editable': True
            }
            return render(request, template, context)
        request.session['mensajeSemillaEditar'] = True
        return redirect('semillaDetalle', idModulo, idSemilla)