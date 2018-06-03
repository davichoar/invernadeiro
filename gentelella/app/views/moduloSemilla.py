from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime
from django.template import loader
from django.urls import reverse

from app.models import Zona, Tipozona, Historiainvernadero, Historiazona, Modulosemilla


def crear(request,
          template='app/modulosemilla/crear.html',
          extra_context=None):
    idTipoZonasSemillas = 1
    listaZonas = Zona.objects.filter(idtipozona = idTipoZonasSemillas,habilitado=True)
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
                mensajeError = "No se puede crear la zona en este momento"
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
    listaZonas = []
    if request.method == 'GET':

        print('LISTAR ZONAS INVERNADERO')

        idInvernadero = int(request.session.get('idInvernadero'))

        try:
            ultimaHistoria = Historiainvernadero.objects.filter(idinvernadero=idInvernadero).order_by('-fecharegistro')[0]
        except:
            ultimaHistoria = Historiainvernadero()
            ultimaHistoria.nivelenergia = 0
            ultimaHistoria.niveltanqueagua = 0


        if "b_buscar" in request.GET:
            valorBusqueda = request.GET.get('textoBusqueda')
            print(valorBusqueda)
            if(valorBusqueda is None):
                valorBusqueda = ""
            listaZonas = Zona.objects.filter(nombre__icontains=valorBusqueda,habilitado=True)
        else:
            listaZonas = Zona.objects.filter(habilitado=True)


        mensajeCreacion = request.session.pop('mensajeModuloCrear',False)
        mensajeEliminar = request.session.pop('mensajeModuloEliminar', False)

        print(listaZonas)
        context = {"historia":ultimaHistoria,"listaZonas": listaZonas.order_by('idzona'), 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('moduloSemillaCrear')
    context = {}
    return render(request, template, context)

def validarRangoCondiciones(actual,min,max):
    if (actual > min) and (actual < max):
        return True
    else:
        return False


def detalle(request,idModulo):

    template = 'app/modulosemilla/verEditar.html'
    zona = Zona.objects.get(idzona=idZona)
    listaTipoZonas = Tipozona.objects.filter(habilitado=True)


    try:
        historiaZona = Historiazona.objects.filter(idzona=idZona).order_by('-fecharegistro')[0]
    except Exception as e:
        historiaZona = None
        print(e)

    temperaturaok = validarRangoCondiciones(historiaZona.temperatura,zona.temperaturamin,zona.temperaturamax)
    phok = validarRangoCondiciones(historiaZona.ph,zona.phmin,zona.phmax)
    co2ok = validarRangoCondiciones(historiaZona.concentracionco2, zona.concentracionco2min,zona.concentracionco2max)

    if request.method == 'GET':
        print('Mostrar Zona Invernadero')
        context = {"historiaZona":historiaZona,"listaTipoZonas":listaTipoZonas,"zona": zona, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'), "editable":False, "temperaturaok" :temperaturaok,"phok":phok,"co2ok":co2ok}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            print('Editar Zona Invernadero')
            context = {"historiaZona":historiaZona,"listaTipoZonas":listaTipoZonas,"zona": zona, 'nombreUsuario': request.session.get('nomreUsuario'),
                       'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": True,  "temperaturaok" :temperaturaok,"phok":phok,"co2ok":co2ok }
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            print('Aceptar Zona Invernadero')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idZona)
            except Exception as e:
                mensajeError = "No se puede crear la zona en este momento"
                print(e)
            zona = obtenerZonaRequest(request)
            if mensajeError:
                context = {"historiaZona": historiaZona, "listaTipoZonas": listaTipoZonas, "zona": zona,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": True, "mensajeError":mensajeError, "temperaturaok" :temperaturaok,"phok":phok,"co2ok":co2ok}
                return render(request, template, context)
            else:
                temperaturaok = validarRangoCondiciones(historiaZona.temperatura, float(zona.temperaturamin), float(zona.temperaturamax))
                phok = validarRangoCondiciones(historiaZona.ph, float(zona.phmin), float(zona.phmax))
                co2ok = validarRangoCondiciones(historiaZona.concentracionco2, float(zona.concentracionco2min),float(zona.concentracionco2max))

                context = {"historiaZona": historiaZona, "listaTipoZonas": listaTipoZonas, "zona": zona,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,"mostrarModalEditar": True, "temperaturaok" :temperaturaok,"phok":phok,"co2ok":co2ok}
                return render(request, template, context)

        if "b_cancelar" in request.POST :
            context = {"historiaZona": historiaZona, "listaTipoZonas": listaTipoZonas, "zona": zona,
                       'nombreUsuario': request.session.get('nomreUsuario'),
                       'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,  "temperaturaok" :temperaturaok,"phok":phok,"co2ok":co2ok }
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            print("Aceptar Modal")
            try:
                eliminarZona(request, idZona)
                request.session['mensajeZonaEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('zonaInvernaderoListar')
        else:
            return redirect('zonaInvernaderoListar')

def eliminarZona(request,idZona):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    zona,created = Zona.objects.update_or_create(
        idzona=idZona, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    zona.save()
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

    if humTierraMin > humTierraMax:
        return "La humedad de la tierra mínima debe ser menor a la humedad de la tierra máxima"

    if humTierraIdeal != "":
        if (humTierraIdeal > humTierraMin) and (humTierraIdeal < humTierraMax):
            print("Humedad Tierra Ideal Valida")
        else:
            return "La humedad de la tierra ideal debe ser un valor entre el mínimo y el máximo"

    if humAmbMin > humAmbMax:
        return "La humedad del ambiente mínima debe ser menor a la humedad del ambiente máxima"

    if humAmbIdeal != "":
        if (humAmbIdeal > humAmbMin) and (humAmbIdeal < humAmbMax):
            print("Humedad Ambiente Ideal Valida")
        else:
            return "La humedad del ambiente ideal debe ser un valor entre el mínimo y el máximo"

    if co2Min > co2Max:
        return "La concentración de CO2 mínima debe ser menor a la concentración de CO2 máxima"

    if co2Ideal != "":
        if (co2Ideal > co2Min) and (co2Ideal < co2Max):
            print("CO2 Ideal Valida")
        else:
            return "La concentración de CO2 ideal debe ser un valor entre el mínimo y el máximo"


    if nivelAguaMin > nivelAguaMax:
        return "La concentración de CO2 mínima debe ser menor a la concentración de CO2 máxima"

    if nivelAguaIdeal != "":
        if (nivelAguaIdeal > nivelAguaMin) and (nivelAguaIdeal < nivelAguaMax):
            print("Nivel del Agua Ideal Valida")
        else:
            return "EL nivel del agua ideal debe ser un valor entre el mínimo y el máximo"

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
        "habilitado":True,
        "idusuarioauditado":idUsuarioActual}
    )

    modulo.save()

    return None

