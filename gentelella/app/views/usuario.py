from django.shortcuts import render, redirect
from app.models import Usuario
from datetime import datetime
import datetime as dt
from django.db.models import Max

def crear(request, template='app/crearUsuario.html', extra_context=None):
    if request.method == 'GET':
        print('nada ps')
        context = { }
        return render(request, template, context)
    elif request.method == 'POST':
        print('no llega aca imbecil')
        if 'b_aceptar' in request.POST:
            nuevoid = Usuario.objects.all().aggregate(Max('idusuario'))['idusuario__max'] + 1
            if 'sexof' in request.POST:
                nuevosexo = 'F'
            elif 'sexom' in request.POST:
                nuevosexo = 'M'
            cadfecha = str(request.POST.get('fechanac'))
            dia, mes, anno = cadfecha.split('/')
            fechanacimientoshida = dt.date(int(anno),int(mes),int(dia))
            if True:
                nuevoUsuario = Usuario.objects.create(
                    idusuario = nuevoid,
                    idrol = 1,
                    nombres = str(request.POST.get('nombre')),
                    apellidopaterno = str(request.POST.get('apepato')),
                    apellidomaterno = str(request.POST.get('apemato')),
                    sexo = nuevosexo,
                    fechanacimiento = fechanacimientoshida,
                    nombreusuario = str(request.POST.get('nombreUsuario')),
                    contrasena = str(request.POST.get('contrasena')),
                    correo = str(request.POST.get('correo')),
                    fechacreacion = datetime.now(),
                    idusuarioauditado = request.session['idUsuarioActual']
                )
            print('cree un usuario xd')
        context = { }
        return render(request, template, context)