from django.shortcuts import render, redirect
from app.models import Usuario, Invernadero, Rol, Usuarioxinvernadero
from datetime import datetime
import datetime as dt
from django.db.models import Max

def crear(request, template='app/usuario/crearUsuario.html', extra_context=None):
    if request.method == 'GET':
        listaRoles = Rol.objects.filter(habilitado=True)
        listaInvernaderos = Invernadero.objects.filter(habilitado=True)
        context = { 'listaRoles': listaRoles, 'listaInvernaderos': listaInvernaderos, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero') }
        return render(request, template, context)
    elif request.method == 'POST':
        nuevoid = Usuario.objects.all().aggregate(Max('idusuario'))['idusuario__max'] + 1
        cadfecha = str(request.POST.get('fechanac'))
        dia, mes, anno = cadfecha.split('/')
        fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
        print(fechanacimientoshida)
        if True:
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
                idusuarioauditado = request.session['idUsuarioActual']
            )
            for inv in request.POST.getlist('invernaderos'):
                usuxinv = Usuarioxinvernadero.objects.create(idinvernadero = inv, idusuario = nuevoid)
        context = { }
        request.session['mensajeUsuarioCrear'] = True
        return redirect('usuariosLista')
        
def listar(request, template='app/usuario/listaUsuarios.html', extra_context=None):
    if request.method == 'GET':
        mostrarModalCrear = request.session.pop('mensajeUsuarioCrear', False)
        mostrarModalEliminar = request.session.pop('mensajeUsuarioEliminar', False)
        listaUsuarios = Usuario.objects.filter(habilitado = True)
        listaRoles = Rol.objects.filter(habilitado=True)
        context = { 'listaUsuarios': list(i for i in zip(range(1,len(listaUsuarios)+1), listaUsuarios)), 'listaRoles': listaRoles,
                    'nombreUsuario': request.session.get('nomreUsuario'), 'nombreInvernadero': request.session.get('nombreInvernadero'), 
                    'mostrarModalCrear': mostrarModalCrear, 'mostrarModalEliminar': mostrarModalEliminar }
        return render(request, template, context)
        
def detalle(request,idUsuario):
    template = 'app/usuario/verEditarUsuario.html'
    usuario = Usuario.objects.get(idusuario = idUsuario)
    listaRoles = Rol.objects.filter(habilitado=True)
    listaInvernaderos = Invernadero.objects.filter(habilitado=True)
    InvernaderosUsuario = Usuarioxinvernadero.objects.filter(idusuario = idUsuario)
    fechaFormateada = usuario.fechanacimiento.strftime('%d/%m/%Y')
    listaInvernaderosUsuario = []
    for usuarioxinvernadero in InvernaderosUsuario:
        listaInvernaderosUsuario.append(usuarioxinvernadero.idinvernadero)
    if request.method == 'GET':
        mostrarModalEditar = request.session.pop('mensajeUsuarioEditar', False)
        print(mostrarModalEditar)
        context = {'listaInvernaderos': listaInvernaderos, 'nombreUsuario': request.session.get('nomreUsuario'), 'fechaFormateada': fechaFormateada, 'nombreInvernadero': request.session.get('nombreInvernadero'), 
        'listaRoles': listaRoles, 'listaInvernaderos': listaInvernaderos, 'listaInvernaderosUsuario': listaInvernaderosUsuario, 'usuario': usuario, 'editable': False, 'mostrarModalEditar': mostrarModalEditar }
        return render(request, template, context)
    if request.method == 'POST':
        if 'b_editar' in request.POST:
            context = {'listaInvernaderos': listaInvernaderos, 'nombreUsuario': request.session.get('nomreUsuario'), 'fechaFormateada': fechaFormateada, 'nombreInvernadero': request.session.get('nombreInvernadero'), 
            'listaRoles': listaRoles, 'listaInvernaderos': listaInvernaderos, 'listaInvernaderosUsuario': listaInvernaderosUsuario, 'usuario': usuario, 'editable': True}
            return render(request, template, context)
        if 'b_aceptar_modal' in request.POST:
            try:
                Usuario.objects.filter(idusuario = idUsuario).update(habilitado=False, idusuarioauditado=request.session['idUsuarioActual'])
                request.session['mensajeUsuarioEliminar'] = True
            except Exception as e:
                print(e)
            return redirect('usuariosLista')
        cadfecha = str(request.POST.get('fechanac'))
        dia, mes, anno = cadfecha.split('/')
        fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
        if True:
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
        request.session['mensajeUsuarioEditar'] = True
        return redirect('usuarioDetalle', idUsuario)
        