from django.shortcuts import render, redirect
from app.models import Usuario, Invernadero, Rol, Usuarioxinvernadero
from datetime import datetime
import datetime as dt
from django.db.models import Max
from django.db import transaction
from app.permissions import *

def mandarWebada(request, cadfecha, idusuario = -1):
    usuarioFake = Usuario()
    usuarioFake.idusuario = idusuario
    usuarioFake.nombres = str(request.POST.get('nombre'))
    usuarioFake.apellidopaterno = str(request.POST.get('apepato'))
    usuarioFake.apellidomaterno = str(request.POST.get('apemato'))
    usuarioFake.idrol = int(request.POST.get('rol'))
    usuarioFake.sexo = request.POST.get('sexo')
    usuarioFake.fechanacimiento = cadfecha,
    usuarioFake.nombreusuario = str(request.POST.get('nombreUsuario'))
    usuarioFake.contrasena = str(request.POST.get('contrasena'))
    usuarioFake.correo = str(request.POST.get('correo'))
    return usuarioFake

def crear(request, template='app/usuario/crearUsuario.html', extra_context=None):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Usuario"):
            return accesodenegado(request)
        listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
        listaInvernaderos = Invernadero.objects.filter(habilitado=True)
        usuarioFake = Usuario()
        usuarioFake.idrol = -1
        usuarioFake.sexo = 'M'
        context = { 
            'listaRoles': listaRoles, 
            'listaInvernaderos': listaInvernaderos, 
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'usuario': usuarioFake
        }
        return render(request, template, context)
    elif request.method == 'POST':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Usuario"):
            return accesodenegado(request)
        nuevoid = Usuario.objects.all().aggregate(Max('idusuario'))['idusuario__max']
        if nuevoid is None:
            nuevoid = 1
        else:
            nuevoid += 1
        cadfecha = str(request.POST.get('fechanac'))
        dia, mes, anno = cadfecha.split('/')
        fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
        if (len(Usuario.objects.filter(habilitado=True, nombreusuario = str(request.POST.get('nombreUsuario')))) > 0):
            listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
            listaInvernaderos = Invernadero.objects.filter(habilitado=True)
            usuarioFake = mandarWebada(request, cadfecha)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'usuario': usuarioFake,
                'mensajeError': 'El nombre de usuario ingresado ya está en uso.',
                'listaRoles': listaRoles,
                'listaInvernaderos': listaInvernaderos,
                'listaInvernaderosUsuario': list(map(int, request.POST.getlist('invernaderos')))
            }
            return render(request, template, context)
        print(fechanacimientoshida)
        try:
            with transaction.atomic():
                nuevoUsuario = Usuario.objects.create(
                    idusuario = nuevoid,
                    idrol = request.POST.get('rol'),
                    nombres = str(request.POST.get('nombre')),
                    apellidopaterno = str(request.POST.get('apepato')),
                    apellidomaterno = str(request.POST.get('apemato')),
                    sexo = request.POST.get('sexo'),
                    fechanacimiento = fechanacimientoshida,
                    nombreusuario = str(request.POST.get('nombreUsuario')),
                    contrasena = str(request.POST.get('contrasena')),
                    correo = str(request.POST.get('correo')),
                    fechacreacion = datetime.now(),
                    idusuarioauditado = request.session['idUsuarioActual'],
                    habilitado = True
                )
                for inv in request.POST.getlist('invernaderos'):
                    usuxinv = Usuarioxinvernadero.objects.create(idinvernadero = inv, idusuario = nuevoid)
        except Exception as e:
            print(e)
            listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
            listaInvernaderos = Invernadero.objects.filter(habilitado=True)
            usuarioFake = mandarWebada(request, cadfecha)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'usuario': usuarioFake,
                'mensajeError': 'Error en la creación del usuario.',
                'listaRoles': listaRoles,
                'listaInvernaderos': listaInvernaderos,
                'listaInvernaderosUsuario': list(map(int, request.POST.getlist('invernaderos')))
            }
            return render(request, template, context)
        request.session['mensajeUsuarioCrear'] = True
        return redirect('usuariosLista')
        
def listar(request, template='app/usuario/listaUsuarios.html', extra_context=None):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Usuario"):
            return accesodenegado(request)
        mostrarModalCrear = request.session.pop('mensajeUsuarioCrear', False)
        mostrarModalEliminar = request.session.pop('mensajeUsuarioEliminar', False)
        listaUsuarios = []
        listaInvernaderoXUsuario = Usuarioxinvernadero.objects.filter(idinvernadero=int(request.session['idInvernadero']))
        for item in listaInvernaderoXUsuario:
            try:
                usuario = Usuario.objects.get(idusuario = item.idusuario, habilitado = True)
            except:
                continue
            listaUsuarios.append(usuario)
        listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
        context = { 
            'listaUsuarios': list(i for i in zip(range(1,len(listaUsuarios)+1), listaUsuarios)),
            'listaRoles': listaRoles,
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'), 
            'mostrarModalCrear': mostrarModalCrear, 
            'mostrarModalEliminar': mostrarModalEliminar 
        }
        return render(request, template, context)
        
def detalle(request,idUsuario):
    template = 'app/usuario/verEditarUsuario.html'
    usuario = Usuario.objects.get(idusuario = idUsuario)
    listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
    listaInvernaderos = Invernadero.objects.filter(habilitado=True)
    InvernaderosUsuario = Usuarioxinvernadero.objects.filter(idusuario = idUsuario)
    fechaFormateada = usuario.fechanacimiento.strftime('%d/%m/%Y')
    listaInvernaderosUsuario = []
    for usuarioxinvernadero in InvernaderosUsuario:
        listaInvernaderosUsuario.append(usuarioxinvernadero.idinvernadero)
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Usuario"):
            return accesodenegado(request)
        mostrarModalEditar = request.session.pop('mensajeUsuarioEditar', False)
        mostrarModalEliminarFallo = request.session.pop('mensajeUsuarioEliminarFallo', False)
        context = {
            'listaInvernaderos': listaInvernaderos,
            'nombreUsuario': request.session.get('nomreUsuario'), 
            'fechaFormateada': fechaFormateada, 
            'nombreInvernadero': request.session.get('nombreInvernadero'), 
            'listaRoles': listaRoles,
            'listaInvernaderos': listaInvernaderos,
            'listaInvernaderosUsuario': listaInvernaderosUsuario,
            'usuario': usuario,
            'editable': False, 
            'mostrarModalEditar': mostrarModalEditar,
            'mostrarModalEliminarFallo': mostrarModalEliminarFallo
        }
        return render(request, template, context)
    if request.method == 'POST':
        if 'b_editar' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Usuario"):
                return accesodenegado(request)
            context = {
                'listaInvernaderos': listaInvernaderos,
                'nombreUsuario': request.session.get('nomreUsuario'),
                'fechaFormateada': fechaFormateada,
                'nombreInvernadero': request.session.get('nombreInvernadero'), 
                'listaRoles': listaRoles,
                'listaInvernaderosUsuario': listaInvernaderosUsuario,
                'usuario': usuario, 
                'editable': True
            }
            return render(request, template, context)
        if 'b_aceptar_modal' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Eliminar Usuario"):
                return accesodenegado(request)
            print(request.session.get('idUsuarioActual'))
            print(idUsuario)
            print(request.session.get('idUsuarioActual') == idUsuario)
            if (int(request.session.get('idUsuarioActual')) == int(idUsuario)):
                request.session['mensajeUsuarioEliminarFallo'] = True
                return redirect('usuarioDetalle', idUsuario)
            try:
                Usuario.objects.filter(idusuario = idUsuario).update(habilitado=False, idusuarioauditado=request.session['idUsuarioActual'])
                request.session['mensajeUsuarioEliminar'] = True
            except Exception as e:
                print(e)
            return redirect('usuariosLista')
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Editar Usuario"):
            return accesodenegado(request)
        cadfecha = str(request.POST.get('fechanac'))
        dia, mes, anno = cadfecha.split('/')
        fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
        
        if (len(Usuario.objects.filter(habilitado=True, nombreusuario = str(request.POST.get('nombreUsuario'))).exclude(idusuario = idUsuario)) > 0):
            listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
            listaInvernaderos = Invernadero.objects.filter(habilitado=True)
            usuarioFake = mandarWebada(request, cadfecha, idUsuario)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'usuario': usuarioFake,
                'fechaFormateada': cadfecha,
                'mensajeError': 'El nombre de usuario ingresado ya está en uso.',
                'listaRoles': listaRoles,
                'listaInvernaderos': listaInvernaderos,
                'listaInvernaderosUsuario': list(map(int, request.POST.getlist('invernaderos'))),
                'editable': True
            }
            return render(request, template, context)
            
        try:
            with transaction.atomic():
                Usuario.objects.filter(idusuario = idUsuario).update(
                    idrol = request.POST.get('rol'),
                    nombres = str(request.POST.get('nombre')),
                    apellidopaterno = str(request.POST.get('apepato')),
                    apellidomaterno = str(request.POST.get('apemato')),
                    sexo = request.POST.get('sexo'),
                    fechanacimiento = fechanacimientoshida,
                    nombreusuario = str(request.POST.get('nombreUsuario')),
                    contrasena = str(request.POST.get('contrasena')),
                    correo = str(request.POST.get('correo')),
                    idusuarioauditado = request.session['idUsuarioActual']
                )
                Usuarioxinvernadero.objects.filter(idusuario = idUsuario).delete()
                print(request.POST.getlist('invernaderos'))
                for inv in request.POST.getlist('invernaderos'):
                    usuxinv = Usuarioxinvernadero.objects.create(idinvernadero = inv, idusuario = idUsuario)
        except Exception as e:
            print(e)
            listaRoles = Rol.objects.filter(habilitado=True).exclude(idrol=-1)
            listaInvernaderos = Invernadero.objects.filter(habilitado=True)
            usuarioFake = mandarWebada(request, cadfecha, idUsuario)
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'usuario': usuarioFake,
                'mensajeError': 'Error en la edición del usuario.',
                'listaRoles': listaRoles,
                'listaInvernaderos': listaInvernaderos,
                'listaInvernaderosUsuario': list(map(int, request.POST.getlist('invernaderos'))),
                'editable': True
            }
            return render(request, template, context)
        request.session['mensajeUsuarioEditar'] = True
        return redirect('usuarioDetalle', idUsuario)
        