from django.db import transaction
from django.db.models import Max
from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime
from app.permissions import *

from app.models import Zona, Tipoplanta,Planta, Historiaplanta

ID_TIPO_ZONAS_PLANTAS = 2
ID_TODAS_ZONAS = -1
CODIGO_GENERAL_COMBO = -1
def crear(request,
          template='app/planta/crear.html',
          extra_context=None):

    try:
        listaTipoPlantas = Tipoplanta.objects.filter(habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePlantaCrearEditarError'] = True ###Revisa esta webada q1
        return redirect('plantaListar')


    try:
        idInvernadero = int(request.session.get('idInvernadero'))
        listaZonas = Zona.objects.filter(idinvernadero=idInvernadero, idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePlantaCrearError'] = True
        return redirect('plantaListar')

    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Planta"):
            return accesodenegado(request)
        print('CREAR PLANTAS')
        context = {'listaTipoPlantas': listaTipoPlantas,
                   'listaZonas':listaZonas,
                   'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),
                   }
        return render(request, template, context)
    elif request.method == 'POST':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Planta"):
            return accesodenegado(request)

        if "b_aceptar" in request.POST:

            mensajeError = None
            try:
               mensajeError = grabarData(request,None)
            except Exception as e:
                mensajeError = "No se puede crear la planta en este momento"
                print(e)

            if mensajeError is not None:
                print("MENSAJE ERROR CREAR PLANTA")
                try:
                    planta = obtenerPlantaRequest(request)
                except Exception as e:
                    print(e)
                    print("Error obteniendo la data del request")
                    planta = None

                context = {"planta":planta,
                           'listaTipoPlantas': listaTipoPlantas,
                           'listaZonas': listaZonas,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'),
                           'mensajeError': mensajeError,
                           }
                return render(request, template, context)
            else:
                request.session['mensajePlantaCrear'] = True
        return redirect('plantaListar')
    else:
        return redirect('plantaListar')


def listar(request,
          extra_context=None):
    #template = loader.get_template('app/zonainvernadero/lista.html')
    template = "app/planta/lista.html"
    listaPlantas = []
    listaTipoPlantas = Tipoplanta.objects.filter(habilitado=True)
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('login')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Planta"):
            return accesodenegado(request)

        print('LISTAR PLANTAS')
        listaIdZonas = []
        try:
            zonaSeleccionada = request.GET.get('comboZona')
        except Exception as e:
            print(e)
            zonaSeleccionada = None
        print('Zona seleccionada --')
        print(zonaSeleccionada)
        try:
            idInvernadero = int(request.session.get('idInvernadero'))
            listaZonas = Zona.objects.filter(idinvernadero=idInvernadero,idtipozona = ID_TIPO_ZONAS_PLANTAS, habilitado=True)
            if zonaSeleccionada == None or int(zonaSeleccionada) == -1:
                for zona in listaZonas:
                    listaIdZonas.append(zona.idzona)
            else:
                listaIdZonas.append(zonaSeleccionada)
        except Exception as e:
            print(e)
            listaZonas = None


        mensajeEliminar = False
        mensajeObtenerZonaError = False
        mensajeCreacion = False
        mensajePlantaCrearEditarError = False

        if listaIdZonas != None:
            if "b_buscar" in request.GET:
                valorBusqueda = request.GET.get('textoBusqueda')
                print(valorBusqueda)
                if (valorBusqueda is None):
                    valorBusqueda = ""
                try:

                    listaTipoPlantas = Tipoplanta.objects.filter(nombrecomun__icontains=valorBusqueda, habilitado=True)
                    listaIdTipoPlanta = []
                    for tipoPlanta in listaTipoPlantas:
                        listaIdTipoPlanta.append(tipoPlanta.idtipoplanta)
                    listaPlantas = Planta.objects.filter(idtipoplanta__in = listaIdTipoPlanta,idzona__in = listaIdZonas, habilitado=True)
                except Exception as e:
                    print(e)
                    listaPlantas = None
            else:
                try:
                    listaPlantas = Planta.objects.filter(idzona__in = listaIdZonas,habilitado=True)
                except Exception as e:
                    print(e)
                    listaPlantas = None

            mensajeCreacion = request.session.pop('mensajePlantaCrear', False)
            mensajeEliminar = request.session.pop('mensajePlantaEliminar', False)
            mensajePlantaCrearEditarError = request.session.pop('mensajePlantaCrearEditarError', False)

            if listaPlantas:
                listaPlantas = listaPlantas.order_by('idplanta')

        else:
            mensajeObtenerZonaError = True
            zonaSeleccionada = ID_TODAS_ZONAS

        print('Lista de plantas')
        print(listaPlantas)
        print(zonaSeleccionada)
        if zonaSeleccionada != None:
            zonaSeleccionada = int(zonaSeleccionada)
        context = {"idseleccionado":zonaSeleccionada,"listaZonas":listaZonas,"listaTipoPlantas":listaTipoPlantas,"listaPlantas": listaPlantas, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,"mensajePlantaCrearEditarError":mensajePlantaCrearEditarError,"mensajeObtenerZonaError":mensajeObtenerZonaError}
        with connection.cursor() as cursor:
            cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto;")
            listaFotos = cursor.fetchall()
        context['listaFotos'] = listaFotos
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('plantaCrear')
    ###Me parece q podriamos borrar toda esta webada de abajo
    if not 'idUsuarioActual' in request.session:
        return redirect('login')
    if not 'idInvernadero' in request.session:
        return redirect('escogerInvernadero')
    if not tienepermiso(request, "Ver Planta"):
        return accesodenegado(request)
    context = {}
    return render(request, template, context)

def validarRangoCondiciones(actual,min,max):

    actual = float(actual)
    min = float(min)
    max = float(max)
    if (actual > min) and (actual < max):
        return True
    else:
        return False


def detalle(request,idPlanta):

    template = 'app/planta/verEditar.html'
    planta = Planta.objects.get(idplanta=idPlanta)

    listaTipoPlantas = Tipoplanta.objects.filter(habilitado=True)
    try:
        idInvernadero = int(request.session.get('idInvernadero'))
        listaZonas = Zona.objects.filter(idinvernadero=idInvernadero, idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePlantaCrearEditarError'] = True
        return redirect('plantaListar')


    try:
        historiaPlanta = Historiaplanta.objects.filter(idplanta=idPlanta).order_by('-fecharegistro')[0]
    except Exception as e:
        historiaPlanta = None
        print(e)

    if historiaPlanta:
        humedadok = validarRangoCondiciones(historiaPlanta.humedad,planta.humedadmin,planta.humedadmax)
    else:
        humedadok = None

    context = {"historiaPlanta": historiaPlanta,"listaTipoPlantas":listaTipoPlantas , "listaZonas": listaZonas, "planta": planta,
               'nombreUsuario': request.session.get('nomreUsuario'),
               'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,
               "humedadok": humedadok}

    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('login')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Planta"):
            return accesodenegado(request)
        print('Mostrar Planta')
        ## context es el mismo de arriba
        context['editable'] = False ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
        tipoPlanta = Tipoplanta.objects.get(idtipoplanta = planta.idtipoplanta)
        with connection.cursor() as cursor:
            cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto and app_tipoplanta.idtipoplanta = %s;", [tipoPlanta.idtipoplanta])
            listaFotos = cursor.fetchall()
        context['tipoPlanta'] = tipoPlanta
        context['listaFotos'] = listaFotos
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('login')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Planta"):
                return accesodenegado(request)
            print('Editar Planta')
            context['editable'] = True
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('login')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Planta"):
                return accesodenegado(request)
            print('Aceptar Planta')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idPlanta)
            except Exception as e:
                mensajeError = "No se puede editar la planta en este momento"
                print(e)

            try:
                planta = obtenerPlantaRequest(request)
            except Exception as e:
                print(e)
                print("Error obteniendo la data del request")
                if mensajeError is not None:
                    mensajeError = "Ocurrió un error inesperado. Intente editar más tarde"

            context['planta'] = planta
            if mensajeError:

                context['editable'] = True
                context['mensajeError'] = mensajeError

                return render(request, template, context)
            else:
                if historiaPlanta:
                    humedadok = validarRangoCondiciones(historiaPlanta.humedad, planta.humedadmin, planta.humedadmax)
                else:
                    humedadok = None

                context['editable'] = False
                context['mostrarModalEditar'] = True
                context['humedadok'] = humedadok
                tipoPlanta = Tipoplanta.objects.get(idtipoplanta = planta.idtipoplanta)
                with connection.cursor() as cursor:
                    cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto and app_tipoplanta.idtipoplanta = %s;", [tipoPlanta.idtipoplanta])
                    listaFotos = cursor.fetchall()
                context['tipoPlanta'] = tipoPlanta
                context['listaFotos'] = listaFotos

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            if not 'idUsuarioActual' in request.session:
                return redirect('login')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Ver Planta"):
                return accesodenegado(request)
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            tipoPlanta = Tipoplanta.objects.get(idtipoplanta = planta.idtipoplanta)
            with connection.cursor() as cursor:
                cursor.execute("select app_tipoplanta.idtipoplanta, app_foto.nombresinextension || app_foto.extension from app_foto, app_tipoplanta where app_tipoplanta.idfoto = app_foto.idfoto and app_tipoplanta.idtipoplanta = %s;", [tipoPlanta.idtipoplanta])
                listaFotos = cursor.fetchall()
            context['tipoPlanta'] = tipoPlanta
            context['listaFotos'] = listaFotos
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('login')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Eliminar Planta"):
                return accesodenegado(request)
            print("Aceptar Modal")
            try:
                eliminarPlanta(request, idPlanta)
                request.session['mensajePlantaEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('plantaListar')
        else:
            return redirect('plantaListar')

def eliminarPlanta(request,idPlanta):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    planta,created = Planta.objects.update_or_create(
        idplanta=idPlanta, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    return


def obtenerPlantaRequest(request):
    plantaDataLlenada = Planta()

    idTipoPlanta = request.POST.get('tipoPlanta')
    idzona = request.POST.get('zona')
    codigoPlanta = request.POST.get('codigoPlanta')
    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')

    if idTipoPlanta != None:
        plantaDataLlenada.idtipoplanta = int(idTipoPlanta)

    if idzona != None:
        plantaDataLlenada.idzona = int(idzona)

    plantaDataLlenada.codigoplantajson = codigoPlanta
    plantaDataLlenada.humedadideal = humedadIdeal
    plantaDataLlenada.humedadmin = humedadMin
    plantaDataLlenada.humedadmax = humedadMax

    return plantaDataLlenada

def grabarData(request,idPlanta):
    print('GRABAR DATA')

    idTipoPlanta = request.POST.get('tipoPlanta')
    idzona = request.POST.get('zona')
    codigoPlanta = request.POST.get('codigoPlanta')
    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')


    if idTipoPlanta:
        print('Tipo Planta correcto')
        idTipoPlanta = int(idTipoPlanta)
    else:
        return "Falta seleccionar el tipo de planta."

    if idTipoPlanta == CODIGO_GENERAL_COMBO:
        return "Falta seleccionar el tipo de planta."

    if idzona:
        idzona = int(idzona)
    else:
        return "Falta seleccionar la zona para la planta"

    if idzona == CODIGO_GENERAL_COMBO:
        return "Falta seleccionar la zona para la planta"

    if codigoPlanta == "":
        return "Falta ingresar el código para la planta."
    else:
        try:
            codigoPlanta = int(codigoPlanta)
        except Exception as e:
            print(e)
            return "Debe ingresar un numero entero para el código de planta"
        if codigoPlanta < 0:
            return "El código de planta debe ser mayor a cero"


    if humedadMin == "":
        return "Falta ingresar la humedad mínima para la planta."

    humedadMin = float(humedadMin)
    if humedadMax == "":
        return "Falta ingresar la humedad máxima para la planta."

    humedadMax = float(humedadMax)
    if humedadMin > humedadMax:
        return "La humedad mínima debe ser menor a la humedad máxima"

    if humedadIdeal != "":
        humedadIdeal = float(humedadIdeal)
        if (humedadIdeal > humedadMin) and (humedadIdeal < humedadMax):
            print("Humedad Ideal Valida")
        else:
            return "La humedad ideal debe ser un valor entre la mínima y la máxima"
    else:
        humedadIdeal = None


    idUsuarioObtenido = request.session.get('idUsuarioActual')
    if idUsuarioObtenido == "" or idUsuarioObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."
    idUsuarioActual = int(idUsuarioObtenido)

    plantaObtenidaBd = None
    if idPlanta is None:
        idMax = Planta.objects.all().aggregate(Max('idplanta'))['idplanta__max']
        if idMax is None:
            idPlanta = 1
        else:
            idPlanta = idMax + 1
        plantaObtenidaBd = Planta.objects.filter(codigoplantajson=codigoPlanta, habilitado=True)

    else:
        plantaObtenidaBd = Planta.objects.filter(codigoplantajson=codigoPlanta, habilitado=True).exclude(idplanta=idPlanta)
        print(plantaObtenidaBd)
    if plantaObtenidaBd.exists():
        return "Ya existe el codigo de planta. Ingrese un codigo de planta distinto"

    with transaction.atomic():
        planta,created = Planta.objects.update_or_create(
            idplanta=idPlanta, defaults={
            "idtipoplanta":idTipoPlanta,
            "idzona":idzona,
            "codigoplantajson" :codigoPlanta,
            "fechacreacion" :datetime.now(),
            "humedadmin":humedadMin,
            "humedadideal":humedadIdeal,
            "humedadmax":humedadMax,
            "habilitado":True,
            "idusuarioauditado":idUsuarioActual}
        )

    return None

