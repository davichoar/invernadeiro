from django.shortcuts import render, redirect
from app.models import Tipoplanta, Foto, Semilla, Planta
from django.conf import settings
from django.db.models import Max
from django.db import transaction
from django.db import connection
from datetime import datetime
from app.permissions import *
import os

def listar(request, template='app/tipoPlanta/listaTipoPlanta.html'):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Tipoplanta"):
            return accesodenegado(request)
        with connection.cursor() as cursor:
            cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto;")
            listaFotos = cursor.fetchall()
        mostrarModalCrear = request.session.pop('mensajeTipoPlantaCrear', False)
        mostrarModalEliminar = request.session.pop('mensajeTipoPlantaEliminar', False)
        context = {
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'listaTipoPlanta': Tipoplanta.objects.filter(habilitado=True),
            'listaFotos': listaFotos,
            'mostrarModalCrear': mostrarModalCrear, 
            'mostrarModalEliminar': mostrarModalEliminar 
        }
        return render(request, template, context)
    
def crear(request, template='app/tipoPlanta/crearTipoPlanta.html'):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Tipoplanta"):
            return accesodenegado(request)
        context = {
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero')    
        }
        return render(request, template, context)
    if request.method == 'POST':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Tipoplanta"):
            return accesodenegado(request)
        nuevoid = Tipoplanta.objects.all().aggregate(Max('idtipoplanta'))['idtipoplanta__max']
        if nuevoid is None:
            nuevoid = 0
        nuevoid += 1
        if 'foto' in request.FILES:
            nuevoidfoto = Foto.objects.all().aggregate(Max('idfoto'))['idfoto__max']
            if nuevoidfoto is None:
                nuevoidfoto = 0
            nuevoidfoto += 1
            rutaFinal=os.path.join(settings.BASE_DIR,'app/static/fotos_tipo_planta/')
            foto = request.FILES['foto']
            filename, extension = os.path.splitext(foto.name)
            nombreArch = str(nuevoid)
            rutaArchivo = os.path.join(rutaFinal, nombreArch + extension)
            with open(rutaArchivo, 'wb+') as f:
                for chunk in foto.chunks():
                    f.write(chunk)
            hayFoto = True
        else:
            hayFoto = False
        try:
            with transaction.atomic():
                if hayFoto:
                    nuevaFoto = Foto.objects.create(
                        idfoto = nuevoidfoto,
                        idmodulo = None,
                        ruta = rutaArchivo,
                        nombresinextension = nombreArch,
                        extension = extension,
                        nombrefoto = nombreArch + extension,
                        fecharegistro = datetime.now() #maybe a corregir.
                    )
                    nuevoTipoPlanta = Tipoplanta.objects.create(
                        idtipoplanta = nuevoid,
                        nombrecomun = str(request.POST.get('nombreComun')),
                        nombrecientifico = str(request.POST.get('nombreCientifico')),
                        idusuarioauditado = request.session['idUsuarioActual'],
                        idfoto = nuevoidfoto,
                        habilitado = True
                    )
                else:
                    nuevoTipoPlanta = Tipoplanta.objects.create(
                        idtipoplanta = nuevoid,
                        nombrecomun = str(request.POST.get('nombreComun')),
                        nombrecientifico = str(request.POST.get('nombreCientifico')),
                        idusuarioauditado = request.session['idUsuarioActual'],
                        habilitado = True
                    )
        except Exception as e:
            tipoPlantaFake = Tipoplanta()
            tipoPlantaFake.nombrecomun = str(request.POST.get('nombreComun'))
            tipoPlantaFake.nombrecientifico = str(request.POST.get('nombreCientifico'))
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'tipoPlanta': tipoPlantaFake,
                'mensajeError': 'Error en la creación del tipo de planta.'
            }
            print(e)
            return render(request, template, context)
        request.session['mensajeTipoPlantaCrear'] = True
        return redirect('tipoPlantaListar')
        
def detalle(request, idTipoPlanta, template = 'app/tipoPlanta/verEditarTipoPlanta.html'):
    tipoPlanta = Tipoplanta.objects.get(idtipoplanta = idTipoPlanta)
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Tipoplanta"):
            return accesodenegado(request)
        with connection.cursor() as cursor:
            cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto and app_tipoplanta.idtipoplanta = %s;", [tipoPlanta.idtipoplanta])
            listaFotos = cursor.fetchall()
        mostrarModalEditar = request.session.pop('mensajeTipoPlantaEditar', False)
        mostrarModalEliminarFallo = request.session.pop('mensajeTipoPlantaEliminarFallo', False)
        context = {
            'nombreUsuario': request.session.get('nomreUsuario'),
            'nombreInvernadero': request.session.get('nombreInvernadero'),
            'tipoPlanta': tipoPlanta,  
            'listaFotos': listaFotos,
            'editable': False, 
            'mostrarModalEditar': mostrarModalEditar,
            'mostrarModalEliminarFallo': mostrarModalEliminarFallo
        }
        return render(request, template, context)
    elif request.method == 'POST':
        if 'b_editar' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Tipoplanta"):
                return accesodenegado(request)
            with connection.cursor() as cursor:
                cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto and app_tipoplanta.idtipoplanta = %s;", [tipoPlanta.idtipoplanta])
                listaFotos = cursor.fetchall()
            context = {
                'nombreUsuario': request.session.get('nomreUsuario'),
                'nombreInvernadero': request.session.get('nombreInvernadero'),
                'tipoPlanta': tipoPlanta,  
                'listaFotos': listaFotos,
                'editable': True
            }
            return render(request, template, context)
        if 'b_aceptar_modal' in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Eliminar Tipoplanta"):
                return accesodenegado(request)
            if (len(Semilla.objects.filter(idtipoplanta = idTipoPlanta, habilitado = True)) > 0 or len(Planta.objects.filter(idtipoplanta = idTipoPlanta, habilitado = True)) > 0):
                request.session['mensajeTipoPlantaEliminarFallo'] = True
                return redirect('tipoPlantaDetalle', idTipoPlanta)
            try:
                Tipoplanta.objects.filter(idtipoplanta = idTipoPlanta).update(habilitado = False, idusuarioauditado=request.session['idUsuarioActual'])
                #Tal vez sea buena idea eliminar tmbn la foto del sistema de archivos aqui
                request.session['mensajeTipoPlantaEliminar'] = True
            except Exception as e:
                print(e)
            return redirect('tipoPlantaListar')
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Editar Tipoplanta"):
            return accesodenegado(request)
        if 'foto' in request.FILES:
            yaTieneFoto = (tipoPlanta.idfoto != None)
            print(yaTieneFoto)
            if not yaTieneFoto:
                nuevoidfoto = Foto.objects.all().aggregate(Max('idfoto'))['idfoto__max']
                if nuevoidfoto is None:
                    nuevoidfoto = 0
                nuevoidfoto += 1
            rutaFinal=os.path.join(settings.BASE_DIR,'app/static/fotos_tipo_planta/')
            foto = request.FILES['foto']
            filename, extension = os.path.splitext(foto.name)
            nombreArch = str(idTipoPlanta)
            rutaArchivo = os.path.join(rutaFinal, nombreArch + extension)
            with open(rutaArchivo, 'wb+') as f:
                for chunk in foto.chunks():
                    f.write(chunk)
            subioFoto = True
        else:
            subioFoto = False
        try:
            with transaction.atomic():
                if subioFoto:
                    if yaTieneFoto:
                        nuevaFoto = Foto.objects.filter(idfoto = tipoPlanta.idfoto).update(
                            ruta = rutaArchivo,
                            nombresinextension = nombreArch,
                            extension = extension,
                            nombrefoto = nombreArch + extension,
                            fecharegistro = datetime.now() #maybe a corregir.
                        )
                        nuevoidfoto = tipoPlanta.idfoto
                    else:
                        nuevaFoto = Foto.objects.create(
                            idfoto = nuevoidfoto,
                            idmodulo = None,
                            ruta = rutaArchivo,
                            nombresinextension = nombreArch,
                            extension = extension,
                            nombrefoto = nombreArch + extension,
                            fecharegistro = datetime.now() #maybe a corregir.
                        )                    
                    Tipoplanta.objects.filter(idtipoplanta = idTipoPlanta).update(
                        nombrecomun = str(request.POST.get('nombreComun')),
                        nombrecientifico = str(request.POST.get('nombreCientifico')),
                        idusuarioauditado = request.session['idUsuarioActual'],
                        idfoto = nuevoidfoto
                    )
                else:
                    Tipoplanta.objects.filter(idtipoplanta = idTipoPlanta).update(
                        nombrecomun = str(request.POST.get('nombreComun')),
                        nombrecientifico = str(request.POST.get('nombreCientifico')),
                        idusuarioauditado = request.session['idUsuarioActual']
                    )
        except Exception as e:
            print(e)
        request.session['mensajeTipoPlantaEditar'] = True
        return redirect('tipoPlantaDetalle', idTipoPlanta)