from django.db.models import Max
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime

from app.models import Zona, Tipozona, Historiainvernadero, Historiazona, Modulosemilla, Historiamodulo, Tipoplanta, \
    Planta

ID_TIPO_ZONAS_PLANTAS = 2
def crear(request,
          template='app/planta/crear.html',
          extra_context=None):
    listaTipoPlantas = Tipoplanta.objects.filter(habilitado=True)
    listaZonas = Zona.objects.filter(idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
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
                mensajeError = "No se puede crear el modulo en este momento"
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
        return redirect('moduloSemillaListar')
    else:
        return redirect('moduloSemillaListar')


def listar(request,
          extra_context=None):
    #template = loader.get_template('app/zonainvernadero/lista.html')
    template = "app/planta/lista.html"
    listaModulos = []
    if request.method == 'GET':

        print('LISTAR MODULOS SEMILLAS')

        if "b_buscar" in request.GET:
            valorBusqueda = request.GET.get('textoBusqueda')
            print(valorBusqueda)
            if(valorBusqueda is None):
                valorBusqueda = ""
            listaModulos = Modulosemilla.objects.filter(nombre__icontains=valorBusqueda,habilitado=True)
        else:
            listaModulos = Modulosemilla.objects.filter(habilitado=True)


        mensajeCreacion = request.session.pop('mensajeModuloCrear',False)
        mensajeEliminar = request.session.pop('mensajeModuloEliminar', False)

        print('Lista de modulos')
        print(listaModulos)
        context = {"listaModulos": listaModulos.order_by('idmodulo'), 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('moduloSemillaCrear')
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


def detalle(request,idModulo):

    template = 'app/planta/verEditar.html'
    modulo = Modulosemilla.objects.get(idmodulo=idModulo)

    listaZonas = Zona.objects.filter(idtipozona = ID_TIPO_ZONAS_SEMILLAS,habilitado=True)


    try:
        historiaModulo = Historiamodulo.objects.filter(idmodulo=idModulo).order_by('-fecharegistro')[0]
    except Exception as e:
        historiaModulo = None
        print(e)

    if historiaModulo:
        temperaturaok = validarRangoCondiciones(historiaModulo.temperatura,modulo.temperaturamin,modulo.temperaturamax)
        humedadTierraok = validarRangoCondiciones(historiaModulo.humedadtierra,modulo.humedadtierramin,modulo.humedadtierramax)
        humedadAmbienteok = validarRangoCondiciones(historiaModulo.humedadambiente,modulo.humedadambientemin,modulo.humedadambientemax)
        nivelAguaok = validarRangoCondiciones(historiaModulo.nivelagua,modulo.nivelaguamin,modulo.nivelaguamax)
        co2ok = validarRangoCondiciones(historiaModulo.concentracionco2,modulo.concentracionco2min,modulo.concentracionco2max)
    else:
        temperaturaok = None
        humedadTierraok = None
        humedadAmbienteok = None
        nivelAguaok = None
        co2ok = None

    context = {"historiaModulo": historiaModulo, "listaZonas": listaZonas, "modulo": modulo,
               'nombreUsuario': request.session.get('nomreUsuario'),
               'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,
               "temperaturaok": temperaturaok, "humedadTierraok": humedadTierraok,
               "humedadAmbienteok": humedadAmbienteok, "nivelAguaok": nivelAguaok, "co2ok": co2ok}

    if request.method == 'GET':
        print('Mostrar Modulo de Semilla')
        ## context es el mismo de arriba
        context['editable'] = False ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            print('Editar Modulo Semilla')
            context['editable'] = True
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            print('Aceptar Modulo Semilla')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idModulo)
            except Exception as e:
                mensajeError = "No se puede crear la zona en este momento"
                print(e)
            modulo = obtenerModuloRequest(request)
            context['modulo'] = modulo
            if mensajeError:

                context['editable'] = True
                context['mensajeError'] = mensajeError

                return render(request, template, context)
            else:
                if historiaModulo:
                    temperaturaok = validarRangoCondiciones(historiaModulo.temperatura, modulo.temperaturamin,modulo.temperaturamax)
                    humedadTierraok = validarRangoCondiciones(historiaModulo.humedadtierra, modulo.humedadtierramin,modulo.humedadtierramax)
                    humedadAmbienteok = validarRangoCondiciones(historiaModulo.humedadambiente,modulo.humedadambientemin, modulo.humedadambientemax)
                    nivelAguaok = validarRangoCondiciones(historiaModulo.nivelagua, modulo.nivelaguamin,modulo.nivelaguamax)
                    co2ok = validarRangoCondiciones(historiaModulo.concentracionco2, modulo.concentracionco2min,modulo.concentracionco2max)

                context['editable'] = False
                context['mostrarModalEditar'] = True
                context['temperaturaok'] = temperaturaok
                context['humedadTierraok'] = humedadTierraok
                context['humedadAmbienteok'] = humedadAmbienteok
                context['nivelAguaok'] = nivelAguaok
                context['co2ok'] = co2ok

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            print("Aceptar Modal")
            try:
                eliminarModulo(request, idModulo)
                request.session['mensajeModuloEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('moduloSemillaListar')
        else:
            return redirect('moduloSemillaListar')

def eliminarModulo(request,idModulo):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    modulo,created = Modulosemilla.objects.update_or_create(
        idmodulo=idModulo, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    modulo.save()
    return


def obtenerPlantaRequest(request):
    plantaDataLlenada = Planta()

    tipoPlanta = request.POST.get('tipoPlanta')
    idzona = request.POST.get('zona')
    idSemilla = request.POST.get('semilla')
    codigoPlanta = request.POST.get('codigoPlanta')
    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')


    return plantaDataLlenada

def grabarData(request,idModulo):
    print('GRABAR DATA')

    tipoPlanta = request.POST.get('tipoPlanta')
    idzona = request.POST.get('zona')
    idSemilla = request.POST.get('semilla')
    codigoPlanta = request.POST.get('codigoPlanta')
    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')


    if tipoPlanta:
        print('Tipo Planta correcto')
    else:
        return "Falta ingresar el tipo de planta."

    if idzona:
        idzona = int(idzona)
    else:
        return "Falta seleccionar la zona para el módulo"


    if codigoPlanta == "":
        return "Falta ingresar el codigo para la planta."


    if humedadMin == "":
        return "Falta ingresar la humedad mínima para la planta."

    if humedadMax == "":
        return "Falta ingresar la humedad máxima para la planta."


    if humedadMin > humedadMax:
        return "La humedad mínima debe ser menor a la humedad máxima"

    if humedadIdeal != "":
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
    if idModulo is None:
        idMax = Modulosemilla.objects.all().aggregate(Max('idmodulo'))['idmodulo__max']
        if idMax is None:
            idModulo = 1
        else:
            idModulo = idMax + 1
        moduloObtenidoBd = Modulosemilla.objects.filter(codigomodulojson=codigoModulo, habilitado=True)

    else:
        moduloObtenidoBd = Modulosemilla.objects.filter(codigomodulojson=codigoModulo, habilitado=True).exclude(idmodulo=idModulo)
        print(moduloObtenidoBd)
    if moduloObtenidoBd.exists():
        return "Ya existe el codigo de zona. Ingrese un codigo de zona distinto"

    print('LLEGO A CREAR HASTA AQUI')

    modulo,created = Modulosemilla.objects.update_or_create(
        idmodulo=idModulo, defaults={
        "nombre":nombre,
        "idzona":idzona,
        "codigomodulojson" :codigoModulo,
        "temperaturaideal":tempIdeal,
        "temperaturamin" :tempMin,
        "temperaturamax" :tempMax,
        "humedadtierraideal": humTierraIdeal,
        "humedadtierramin": humTierraMin,
        "humedadtierramax": humTierraMax,
        "humedadambienteideal": humAmbIdeal,
        "humedadambientemin": humAmbMin,
        "humedadambientemax": humAmbMax,
        "concentracionco2ideal":co2Ideal,
        "concentracionco2min":co2Min,
        "concentracionco2max":co2Max,
        "nivelaguaideal": nivelAguaIdeal,
        "nivelaguamin": nivelAguaMin,
        "nivelaguamax": nivelAguaMax,
        "fechacreacion" :datetime.now(),
        "filas":filas,
        "columnas":columnas,
        "habilitado":True,
        "idusuarioauditado":idUsuarioActual}
    )

    modulo.save()

    return None

