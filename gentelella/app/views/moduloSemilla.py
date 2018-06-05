from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime
from django.template import loader
from django.urls import reverse

from app.models import Zona, Tipozona, Historiainvernadero, Historiazona, Modulosemilla, Historiamodulo, Semilla, Historiasemilla, Tipoplanta

ID_TIPO_ZONAS_SEMILLAS = 1
def crear(request,
          template='app/modulosemilla/crear.html',
          extra_context=None):
    listaZonas = Zona.objects.filter(idtipozona = ID_TIPO_ZONAS_SEMILLAS,habilitado=True)
    if request.method == 'GET':
        print('CREAR MODULO DE SEMILLAS')
        context = {'listaZonas': listaZonas,
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
                modulo = obtenerModuloRequest(request)
                context = {"modulo":modulo,
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
    template = "app/modulosemilla/lista.html"
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

        
def contextParaGrilla(context, modulo):
    context['rangeFilas'] = range(1, modulo.filas + 1)
    context['rangeColumnas'] = range(1, modulo.columnas + 1)
    semillas = Semilla.objects.filter(idmodulo=modulo.idmodulo, habilitado=True)
    listaSemillas = dict()
    for semilla in semillas:
        try:
            historiaSemilla = Historiasemilla.objects.filter(idsemilla=semilla.idsemilla).order_by('-fecharegistro')[0]
        except:
            continue
        posx = historiaSemilla.posx
        if not posx in listaSemillas:
            listaSemillas[posx] = dict()
        listaSemillas[posx][historiaSemilla.posy] = (semilla, Tipoplanta.objects.get(idtipoplanta = semilla.idtipoplanta).nombrecomun)
    context['listaSemillas'] = listaSemillas
    print(listaSemillas)

def detalle(request,idModulo):

    template = 'app/modulosemilla/verEditar.html'
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
        contextParaGrilla(context, modulo)
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
                contextParaGrilla(context, modulo)

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            contextParaGrilla(context, modulo)
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


def obtenerModuloRequest(request):
    moduloDataLlenada = Modulosemilla()

    nombreObtenido = request.POST.get('nombre')
    codigoModulo = request.POST.get('codigoModulo')
    idzona = request.POST.get('zona')
    tempIdeal = request.POST.get('tempIdeal')
    tempMin = request.POST.get('tempMin')
    tempMax = request.POST.get('tempMax')
    humTierraIdeal = request.POST.get('humedadTierraIdeal')
    humTierraMin = request.POST.get('humedadTierraMin')
    humTierraMax = request.POST.get('humedadTierraMax')
    humAmbIdeal = request.POST.get('humedadAmbienteIdeal')
    humAmbMin = request.POST.get('humedadAmbienteMin')
    humAmbMax = request.POST.get('humedadAmbienteMax')
    co2Ideal = request.POST.get('co2Ideal')
    co2Min = request.POST.get('co2Min')
    co2Max = request.POST.get('co2Max')
    nivelAguaIdeal = request.POST.get('nivelAguaIdeal')
    nivelAguaMin = request.POST.get('nivelAguaMin')
    nivelAguaMax = request.POST.get('nivelAguaMax')
    filas = request.POST.get('filas')
    columnas = request.POST.get('columnas')


    moduloDataLlenada.nombre = nombreObtenido
    moduloDataLlenada.codigomodulojson = codigoModulo
    moduloDataLlenada.idzona = idzona
    moduloDataLlenada.temperaturaideal = tempIdeal
    moduloDataLlenada.temperaturamin = tempMin
    moduloDataLlenada.temperaturamax = tempMax
    moduloDataLlenada.humedadtierraideal = humTierraIdeal
    moduloDataLlenada.humedadtierramin = humTierraMin
    moduloDataLlenada.humedadtierramax = humTierraMax
    moduloDataLlenada.humedadambienteideal = humAmbIdeal
    moduloDataLlenada.humedadambientemin = humAmbMin
    moduloDataLlenada.humedadambientemax = humAmbMax
    moduloDataLlenada.concentracionco2ideal = co2Ideal
    moduloDataLlenada.concentracionco2min = co2Min
    moduloDataLlenada.concentracionco2max = co2Max
    moduloDataLlenada.nivelaguaideal = nivelAguaIdeal
    moduloDataLlenada.nivelaguamin = nivelAguaMin
    moduloDataLlenada.nivelaguamax = nivelAguaMax
    moduloDataLlenada.filas = filas
    moduloDataLlenada.columnas = columnas

    return moduloDataLlenada

def grabarData(request,idModulo):
    print('GRABAR DATA')

    nombreObtenido = request.POST.get('nombre')
    codigoModuloObtenido = request.POST.get('codigoModulo')
    idzona = request.POST.get('zona')
    tempIdeal = request.POST.get('tempIdeal')
    tempMin = request.POST.get('tempMin')
    tempMax = request.POST.get('tempMax')
    humTierraIdeal = request.POST.get('humedadTierraIdeal')
    humTierraMin = request.POST.get('humedadTierraMin')
    humTierraMax = request.POST.get('humedadTierraMax')
    humAmbIdeal = request.POST.get('humedadAmbienteIdeal')
    humAmbMin = request.POST.get('humedadAmbienteMin')
    humAmbMax = request.POST.get('humedadAmbienteMax')
    co2Ideal = request.POST.get('co2Ideal')
    co2Min = request.POST.get('co2Min')
    co2Max = request.POST.get('co2Max')
    nivelAguaIdeal = request.POST.get('nivelAguaIdeal')
    nivelAguaMin = request.POST.get('nivelAguaMin')
    nivelAguaMax = request.POST.get('nivelAguaMax')
    filas = request.POST.get('filas')
    columnas = request.POST.get('columnas')

    if nombreObtenido:
        nombre = str(nombreObtenido)
    else:
        return "Falta ingresar el nombre del módulo."


    if codigoModuloObtenido:
        codigoModulo = int(codigoModuloObtenido)
    else:
        return "Falta ingresar el codigo para el módulo."

    if idzona:
        idzona = int(idzona)
    else:
        return "Falta seleccionar la zona para el módulo"


    if tempMin == "":
        return "Falta ingresar la temperatura mínima para el módulo."


    if tempMax == "":
        return "Falta ingresar la temperatura máxima para el módulo."


    # if humTierraIdeal == "":
    #     return "Falta ingresar la humedad de la tierra ideal para el módulo."

    if humTierraMin == "":
        return "Falta ingresar la humedad de la tierra mínima para el módulo."

    if humTierraMax == "":
        return "Falta ingresar la humedad de la tierra máxima para el módulo."

    # if humAmbIdeal == "":
    #     return "Falta ingresar la humedad del ambiente ideal para el módulo."

    if humAmbMin == "":
        return "Falta ingresar la humedad del ambiente mínima para el módulo."

    if humAmbMax == "":
        return "Falta ingresar la humedad del ambiente máxima para el módulo."

    #
    # if co2Ideal == "":
    #     return "Falta ingresar la concentración de CO2 ideal para el módulo."


    if co2Min == "":
        return "Falta ingresar la concentración de CO2 mínima para el módulo."


    if co2Max == "":
        return "Falta ingresar la concentración de CO2 máxima para el módulo."

    # if nivelAguaIdeal == "":
    #     return "Falta ingresar el nivel del agua ideal para el módulo."


    if nivelAguaMin == "":
        return "Falta ingresar el nivel del agua mínimo para el módulo."


    if nivelAguaMax == "":
        return "Falta ingresar el nivel del agua máximo para el módulo."


    if filas == "":
        return "Falta ingresar las filas para el módulo."


    if columnas == "":
        return "Falta ingresar las columnas para el módulo."



    if tempMin > tempMax:
        return "La temperatura mínima debe ser menor a la temperatura máxima"

    if tempIdeal != "":
        if (tempIdeal > tempMin) and (tempIdeal < tempMax):
            print("Temperatura Ideal Valida")
        else:
            return "La temperatura ideal debe ser un valor entre la mínima y la máxima"
    else:
        tempIdeal = None

    if humTierraMin > humTierraMax:
        return "La humedad de la tierra mínima debe ser menor a la humedad de la tierra máxima"

    if humTierraIdeal != "":
        if (humTierraIdeal > humTierraMin) and (humTierraIdeal < humTierraMax):
            print("Humedad Tierra Ideal Valida")
        else:
            return "La humedad de la tierra ideal debe ser un valor entre el mínimo y el máximo"
    else:
        humTierraIdeal = None

    if humAmbMin > humAmbMax:
        return "La humedad del ambiente mínima debe ser menor a la humedad del ambiente máxima"

    if humAmbIdeal != "":
        if (humAmbIdeal > humAmbMin) and (humAmbIdeal < humAmbMax):
            print("Humedad Ambiente Ideal Valida")
        else:
            return "La humedad del ambiente ideal debe ser un valor entre el mínimo y el máximo"
    else:
        humAmbIdeal = None

    if co2Min > co2Max:
        return "La concentración de CO2 mínima debe ser menor a la concentración de CO2 máxima"

    if co2Ideal != "":
        if (co2Ideal > co2Min) and (co2Ideal < co2Max):
            print("CO2 Ideal Valida")
        else:
            return "La concentración de CO2 ideal debe ser un valor entre el mínimo y el máximo"
    else:
        co2Ideal = None


    if nivelAguaMin > nivelAguaMax:
        return "El nivel del agua mínimo debe ser menor al nivel del agua máximo"

    if nivelAguaIdeal != "":
        if (nivelAguaIdeal > nivelAguaMin) and (nivelAguaIdeal < nivelAguaMax):
            print("Nivel del Agua Ideal Valida")
        else:
            return "EL nivel del agua ideal debe ser un valor entre el mínimo y el máximo"
    else:
        nivelAguaIdeal = None

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

