from django.db.models import Max
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime

from app.models import Zona, Tipozona, Historiainvernadero, Historiazona, Modulosemilla, Historiamodulo, Tipoplanta, \
    Planta, Semilla, Historiaplanta

ID_TIPO_ZONAS_PLANTAS = 2
def crear(request,
          template='app/planta/crear.html',
          extra_context=None):

    try:
        listaTipoPlantas = Tipoplanta.objects.filter(habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePlantaCrearEditarError'] = True
        return redirect('plantaListar')


    try:
        idInvernadero = int(request.session.get('idInvernadero'))
        listaZonas = Zona.objects.filter(idinvernadero=idInvernadero, idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePlantaCrearError'] = True
        return redirect('plantaListar')

    if request.method == 'GET':
        print('CREAR PLANTAS')
        context = {'listaTipoPlantas': listaTipoPlantas,
                   'listaZonas':listaZonas,
                   'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),
                   }
        return render(request, template, context)
    elif request.method == 'POST':

        if "b_aceptar" in request.POST:

            mensajeError = None
            try:
               mensajeError = grabarData(request,None)
            except Exception as e:
                mensajeError = "No se puede crear la planta en este momento"
                print(e)

            if mensajeError is not None:
                print("MENSAJE ERROR CREAR ZONA")
                planta = obtenerPlantaRequest(request)
                context = {"planta":planta,
                           'listaTipoPlantas': listaTipoPlantas,
                           'listaZonas': listaZonas,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'),
                           'mensajeError': mensajeError,
                           }
                return render(request, template, context)
            else:
                request.session['mensajeModuloCrear'] = True
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

        print('LISTAR PLANTAS')
        listaIdZonas = []
        try:
            idInvernadero = int(request.session.get('idInvernadero'))
            listaZonas = Zona.objects.filter(idinvernadero=idInvernadero,idtipozona = ID_TIPO_ZONAS_PLANTAS, habilitado=True)
            for zona in listaZonas:
                listaIdZonas.append(zona.idzona)
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
                    listaPlantas = Planta.objects.filter(idzona__in = listaIdZonas,nombre__icontains=valorBusqueda, habilitado=True)
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

        print('Lista de plantas')
        print(listaPlantas)
        context = {"listaTipoPlantas":listaTipoPlantas,"listaPlantas": listaPlantas, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,"mensajePlantaCrearEditarError":mensajePlantaCrearEditarError,"mensajeObtenerZonaError":mensajeObtenerZonaError}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('plantaCrear')
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
        print('Mostrar Planta')
        ## context es el mismo de arriba
        context['editable'] = False ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            print('Editar Planta')
            context['editable'] = True
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            print('Aceptar Planta')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idPlanta)
            except Exception as e:
                mensajeError = "No se puede crear la planta en este momento"
                print(e)
            planta = obtenerPlantaRequest(request)
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

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            print("Aceptar Modal")
            try:
                eliminarModulo(request, idPlanta)
                request.session['mensajePlantaEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('plantaListar')
        else:
            return redirect('plantaListar')

def eliminarModulo(request,idModulo):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    modulo,created = Modulosemilla.objects.update_or_create(
        idmodulo=idModulo, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    modulo.save()
    return


def obtenerPlantaRequest(request):
    plantaDataLlenada = Planta()

    idTipoPlanta = request.POST.get('tipoPlanta')
    idzona = request.POST.get('zona')
    codigoPlanta = request.POST.get('codigoPlanta')
    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')


    plantaDataLlenada.idtipoplanta = idTipoPlanta
    plantaDataLlenada.idzona = idzona
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
    else:
        return "Falta ingresar el tipo de planta."

    if idzona:
        idzona = int(idzona)
    else:
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

    moduloObtenidoBd = None
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

    planta.save()

    return None

