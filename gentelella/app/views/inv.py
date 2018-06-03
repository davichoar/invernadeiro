from django.shortcuts import render, redirect
from datetime import datetime
import datetime as dt
from django.db.models import Max
from app.models import Invernadero, Usuario
from django.db import transaction

def crearFake(request, idinvernadero = -1):
    invernaderoFake = Invernadero()
    invernaderoFake.idinvernadero = idinvernadero
    invernaderoFake.nombre = request.POST.get('nombre')
    invernaderoFake.codigoinvernaderojson = request.POST.get('codigoInv')
    invernaderoFake.idadmin = request.POST.get('admin')
    invernaderoFake.area = request.POST.get('area')
    invernaderoFake.niveltanqueaguaideal = request.POST.get('aguaIdeal')
    invernaderoFake.niveltanqueaguamin = request.POST.get('aguaMin')
    invernaderoFake.niveltanqueaguamax = request.POST.get('aguaMax')
    invernaderoFake.nivelenergiaideal = request.POST.get('energiaIdeal')
    invernaderoFake.nivelenergiamin = request.POST.get('energiaMin')
    invernaderoFake.nivelenergiamax = request.POST.get('energiaMax')
    invernaderoFake.latitud = request.POST.get('latitud')
    invernaderoFake.longitud = request.POST.get('longitud')
    return invernaderoFake

def listar(request, template='app/invernadero/listaInvernaderos.html', extra_context=None):
    if request.method == 'GET':
        mostrarModalCrear = request.session.pop('mensajeInvernaderoCrear', False)
        mostrarModalEliminar = request.session.pop('mensajeInvernaderoEliminar', False)        
        if "b_buscar" in request.GET:
            valorBusqueda = request.GET.get('textoBusqueda')
            if(valorBusqueda is None):
                valorBusqueda = ""
            listaInvernaderos = Invernadero.objects.filter(nombre__icontains=valorBusqueda, habilitado=True)
        else:
            listaInvernaderos = Invernadero.objects.filter(habilitado=True)
        context = { 
            'listaInvernaderos': listaInvernaderos,
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'), 
            'mostrarModalCrear': mostrarModalCrear, 
            'mostrarModalEliminar': mostrarModalEliminar 
        }
        return render(request, template, context)
        
def crear(request, template='app/invernadero/crearInvernadero.html', extra_context=None):
    if request.method == 'GET':
        listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
        invernaderoFake = Invernadero()
        invernaderoFake.idadmin = -1
        context = { 
            'listaUsuarios': listaUsuarios, 
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'inv': invernaderoFake
        }
        return render(request, template, context)
    elif request.method == 'POST':
        nuevoid = Invernadero.objects.all().aggregate(Max('idinvernadero'))['idinvernadero__max']
        if nuevoid is None:
            nuevoid = 1
        else:
            nuevoid += 1
        if (len(Invernadero.objects.filter(habilitado=True, codigoinvernaderojson=int(request.POST.get('codigoInv')))) > 0):
            inv = crearFake(request)
            listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
            context = { 
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'listaUsuarios': listaUsuarios, 
                'mensajeError': 'El código de invernadero ingresado ya está en uso.',
                'inv': inv
            }
            return render(request, template, context)
        area = request.POST.get('area')
        if (area == ''):
            area = None
        aguaIdeal = request.POST.get('aguaIdeal')
        if (aguaIdeal == ''):
            aguaIdeal = None
        energiaIdeal = request.POST.get('energiaIdeal')
        if (energiaIdeal == ''):
            energiaIdeal = None
        latitud = request.POST.get('latitud')
        if (latitud == ''):
            latitud = None
        longitud = request.POST.get('longitud')
        if (longitud == ''):
            longitud = None
        try:
            nuevoInvernadero = Invernadero.objects.create(
                idinvernadero = nuevoid,
                nombre = request.POST.get('nombre'),
                codigoinvernaderojson = request.POST.get('codigoInv'),
                idadmin = request.POST.get('admin'),
                area = area,
                niveltanqueaguaideal = aguaIdeal,
                niveltanqueaguamin = request.POST.get('aguaMin'),
                niveltanqueaguamax = request.POST.get('aguaMax'),
                nivelenergiaideal = energiaIdeal,
                nivelenergiamin = request.POST.get('energiaMin'),
                nivelenergiamax = request.POST.get('energiaMax'),
                latitud = latitud,
                longitud = longitud,
                fechacreacion = datetime.now(),
                idusuarioauditado = request.session['idUsuarioActual'],
                habilitado = True
            )
        except Exception as e:
            print(e)
            inv = crearFake(request)
            listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
            context = { 
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'listaUsuarios': listaUsuarios, 
                'mensajeError': 'Error en la creación del invernadero.',
                'inv': inv
            }
            return render(request, template, context)
        request.session['mensajeInvernaderoCrear'] = True
        return redirect('invernaderoLista')
        
        
def detalle(request, idInv):
    template = 'app/invernadero/verEditarInvernadero.html'
    inv = Invernadero.objects.get(idinvernadero = idInv)
    listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
    if request.method == 'GET':
        mostrarModalEditar = request.session.pop('mensajeInvernaderoEditar', False)
        mostrarModalEliminarFallo = request.session.pop('mensajeInvernaderoEliminarFallo', False)
        context = {
            'listaUsuarios': listaUsuarios,
            'nombreUsuario': request.session.get('nomreUsuario'), 
            'nombreInvernadero': request.session.get('nombreInvernadero'), 
            'inv': inv,
            'editable': False, 
            'mostrarModalEditar': mostrarModalEditar,
            'mostrarModalEliminarFallo': mostrarModalEliminarFallo
        }
        return render(request, template, context)
    if request.method == 'POST':
        if 'b_editar' in request.POST:
            context = {
                'listaUsuarios': listaUsuarios,
                'nombreUsuario': request.session.get('nomreUsuario'), 
                'nombreInvernadero': request.session.get('nombreInvernadero'), 
                'inv': inv,
                'editable': True
            }
            return render(request, template, context)
        if 'b_aceptar_modal' in request.POST:
            if (int(request.session.get('idInvernadero')) == int(idInv)):
                request.session['mensajeInvernaderoEliminarFallo'] = True
                return redirect('invernaderoDetalle', idInv)
            try:
                Invernadero.objects.filter(idinvernadero = idInv).update(habilitado=False, idusuarioauditado=request.session['idUsuarioActual'])
                request.session['mensajeInvernaderoEliminar'] = True
            except Exception as e:
                print(e)
            return redirect('invernaderoLista')
        if (len(Invernadero.objects.filter(habilitado=True, codigoinvernaderojson=int(request.POST.get('codigoInv'))).exclude(idinvernadero=idInv)) > 0):
            invFake = crearFake(request, idInv)
            listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
            context = { 
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'listaUsuarios': listaUsuarios, 
                'mensajeError': 'El código de invernadero ingresado ya está en uso.',
                'inv': invFake,
                'editable': True
            }
            return render(request, template, context)
        area = request.POST.get('area')
        if (area == ''):
            area = None
        aguaIdeal = request.POST.get('aguaIdeal')
        if (aguaIdeal == ''):
            aguaIdeal = None
        energiaIdeal = request.POST.get('energiaIdeal')
        if (energiaIdeal == ''):
            energiaIdeal = None
        latitud = request.POST.get('latitud')
        if (latitud == ''):
            latitud = None
        longitud = request.POST.get('longitud')
        if (longitud == ''):
            longitud = None
        try:
            Invernadero.objects.filter(idinvernadero=idInv).update(
                nombre = request.POST.get('nombre'),
                codigoinvernaderojson = request.POST.get('codigoInv'),
                idadmin = request.POST.get('admin'),
                area = area,
                niveltanqueaguaideal = aguaIdeal,
                niveltanqueaguamin = request.POST.get('aguaMin'),
                niveltanqueaguamax = request.POST.get('aguaMax'),
                nivelenergiaideal = energiaIdeal,
                nivelenergiamin = request.POST.get('energiaMin'),
                nivelenergiamax = request.POST.get('energiaMax'),
                latitud = latitud,
                longitud = longitud,
                idusuarioauditado = request.session['idUsuarioActual']
            )
        except Exception as e:
            print(e)
            invFake = crearFake(request, idInv)
            listaUsuarios = Usuario.objects.filter(habilitado=True).exclude(idrol=-1)
            context = { 
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'listaUsuarios': listaUsuarios, 
                'mensajeError': 'Error en la edición del invernadero.',
                'inv': invFake,
                'editable': True
            }
            return render(request, template, context)
        request.session['mensajeInvernaderoEditar'] = True
        return redirect('invernaderoDetalle', idInv)