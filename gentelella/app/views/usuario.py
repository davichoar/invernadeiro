from django.shortcuts import render, redirect
from app.models import Usuario, Invernadero, Rol
from datetime import datetime
import datetime as dt
from django.db.models import Max

def crear(request, template='app/crearUsuario.html', extra_context=None):
    if request.method == 'GET':
        print('nada ps')
        listaRoles = Rol.objects.filter(habilitado=True)
        listaInvernaderos = Invernadero.objects.filter(habilitado=True)
        context = { 'listaRoles': listaRoles, 'listaInvernaderos': listaInvernaderos }
        return render(request, template, context)
    elif request.method == 'POST':
        print('no llega aca imbecil')
        print(request.POST.get('rol'))
        nuevoid = Usuario.objects.all().aggregate(Max('idusuario'))['idusuario__max'] + 1
        cadfecha = str(request.POST.get('fechanac'))
        dia, mes, anno = cadfecha.split('/')
        fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
        print(fechanacimientoshida)
        if False:
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
        print('cree un usuario xd')
        context = { }
        return redirect('usuariosLista')
        
def listar(request, template='app/listaUsuarios.html', extra_context=None):
    if request.method == 'GET':
        print('isi dp2')
        listaUsuarios = Usuario.objects.all() # habilitado falta
        listaRoles = Rol.objects.filter(habilitado=True)
        context = { 'listaUsuarios': list(i for i in zip(range(1,len(listaUsuarios)+1), listaUsuarios)), 'listaRoles': listaRoles }
        return render(request, template, context)