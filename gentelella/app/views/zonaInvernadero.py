from django.db.models import Max
from django.shortcuts import render, redirect
from datetime import datetime
from django.db import transaction
from app.models import Invernadero,Zona, Tipozona, Historiainvernadero, Historiazona,Planta, Modulosemilla, Panelluz
from app.permissions import *

CANTIDAD_CADENA_MAXIMA = 250
CODIGO_GENERAL_COMBO = -1
ID_TIPO_ZONAS_PLANTAS = 2
def crear(request,
          template='app/zonainvernadero/create.html',
          extra_context=None):
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Zona"):
            return accesodenegado(request)
        print('CREAR ZONAS DEL INVERANDERO')
        listaTipoZonas = Tipozona.objects.filter(habilitado = True)
        context = {"listaTipoZonas": listaTipoZonas,
                   'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),
                   }
        return render(request, template, context)
    elif request.method == 'POST':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Crear Zona"):
            return accesodenegado(request)

        idInvernadero = int(request.session.get('idInvernadero'))
        if "b_aceptar" in request.POST:

            mensajeError = None
            try:
                mensajeError = grabarData(request,None)
            except Exception as e:
                mensajeError = "No se puede crear la zona en este momento"
                print(e)

            if mensajeError is not None:
                print("MENSAJE ERROR CREAR ZONA")
                try:
                    zona = obtenerZonaRequest(request)
                except Exception as e:
                    zona = None
                    print(e)
                    print("Error obteniendo la data del request")

                listaTipoZonas = Tipozona.objects.filter(habilitado=True)
                context = {"zona":zona,
                            "listaTipoZonas": listaTipoZonas,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'),
                           'mensajeError': mensajeError,
                           }
                return render(request, template, context)
            else:
                request.session['mensajeZonaCrear'] = True
        return redirect('zonaInvernaderoListar')
    else:
        return redirect('zonaInvernaderoListar')


def listar(request,
          extra_context=None):
    #template = loader.get_template('app/zonainvernadero/lista.html')
    template = "app/zonainvernadero/list.html"
    listaZonas = []
    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Zona"):
            return accesodenegado(request)

        print('LISTAR ZONAS INVERNADERO')

        idInvernadero = int(request.session.get('idInvernadero'))
        invernadero = None
        try:
            invernadero = Invernadero.objects.get(idinvernadero=idInvernadero)
            ultimaHistoria = Historiainvernadero.objects.filter(idinvernadero=idInvernadero).order_by('-fecharegistro')[0]
            nivelAguaok = validarRangoCondiciones(ultimaHistoria.niveltanqueagua,invernadero.niveltanqueaguamin,invernadero.niveltanqueaguamax)
            nivelEnergiaok = validarRangoCondiciones(ultimaHistoria.nivelenergia,invernadero.nivelenergiamin,invernadero.nivelenergiamax)
        except:
            ultimaHistoria = None
            nivelAguaok = None
            nivelEnergiaok = None

        if "b_buscar" in request.GET:
            valorBusqueda = request.GET.get('textoBusqueda')
            print(valorBusqueda)
            if(valorBusqueda is None):
                valorBusqueda = ""
            listaZonas = Zona.objects.filter(idinvernadero=idInvernadero,nombre__icontains=valorBusqueda,habilitado=True)
        else:
            listaZonas = Zona.objects.filter(idinvernadero=idInvernadero,habilitado=True)


        mensajeCreacion = request.session.pop('mensajeZonaCrear',False)
        mensajeEliminar = request.session.pop('mensajeZonaEliminar', False)

        print(listaZonas)
        context = {"historia":ultimaHistoria,"listaZonas": listaZonas.order_by('idzona'), 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,"nivelAguaok":nivelAguaok,"nivelEnergiaok":nivelEnergiaok}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('zonaInvernaderoCrear')
    ###Me parece q podriamos borrar toda esta webada de abajo
    if not 'idUsuarioActual' in request.session:
        return redirect('loginIndex')
    if not 'idInvernadero' in request.session:
        return redirect('escogerInvernadero')
    if not tienepermiso(request, "Ver Zona"):
        return accesodenegado(request)
    context = {}
    return render(request, template, context)

def validarRangoCondiciones(actual,min,max):
    if min == None:
        return True
    if max == None:
        return True

    actual = float(actual)
    min = float(min)
    max = float(max)
    if (actual > min) and (actual < max):
        return True
    else:
        return False


def detalle(request,idZona):

    template = 'app/zonainvernadero/show.html'
    zona = Zona.objects.get(idzona=idZona)
    listaTipoZonas = Tipozona.objects.filter(habilitado=True)

    zonaConPlanta = hayPlantasAsociadasZona(idZona)
    zonaConModulo = hayModulosAsociadasZona(idZona)
    zonaConPanel = hayPanelesAsociadasZona(idZona)
    try:
        historiaZonaTemperatura = Historiazona.objects.filter(idzona=idZona,temperatura__isnull=False).order_by('-fecharegistro')[0]
    except Exception as e:
        print("No hay historia zona para el parametro de temperatura")
        historiaZonaTemperatura = None
        print(e)
    try:
        historiaZonaPh = Historiazona.objects.filter(idzona=idZona, ph__isnull=False).order_by('-fecharegistro')[0]
    except Exception as e:
        print("No hay historia zona para el parametro de ph")
        historiaZonaPh = None
        print(e)

    try:
        historiaZonaCo2 = Historiazona.objects.filter(idzona=idZona, concentracionco2__isnull=False).order_by('-fecharegistro')[0]
    except Exception as e:
        print("No hay historia zona para el parametro de co2")
        historiaZonaCo2 = None
        print(e)

    try:
        historiaZonaHumedad = Historiazona.objects.filter(idzona=idZona, humedad__isnull=False).order_by('-fecharegistro')[0]
    except Exception as e:
        print("No hay historia zona para el parametro de humedad")
        historiaZonaHumedad = None
        print(e)


    hayHistoria = False
    contadorHistoria = 0
    if historiaZonaTemperatura:
        temperaturaok = validarRangoCondiciones(historiaZonaTemperatura.temperatura, zona.temperaturamin, zona.temperaturamax)
        contadorHistoria += 1
    else:
        temperaturaok = None

    if historiaZonaPh:
        phok = validarRangoCondiciones(historiaZonaPh.ph, zona.phmin, zona.phmax)
        contadorHistoria += 1
    else:
        phok = None

    if historiaZonaCo2:
        co2ok = validarRangoCondiciones(historiaZonaCo2.concentracionco2, zona.concentracionco2min,zona.concentracionco2max)
        contadorHistoria += 1
    else:
        co2ok = None

    if historiaZonaHumedad:
        humedadok = validarRangoCondiciones(historiaZonaHumedad.humedad, zona.humedadmin, zona.humedadmax)
        contadorHistoria += 1
    else:
        humedadok = None

    if contadorHistoria > 0:
        hayHistoria = True

    context = {"zonaConPlanta":zonaConPlanta,"zonaConModulo":zonaConModulo,"zonaConPanel":zonaConPanel,"historiaZonaTemperatura": historiaZonaTemperatura,"historiaZonaPh":historiaZonaPh, "historiaZonaCo2":historiaZonaCo2, "historiaZonaHumedad":historiaZonaHumedad ,"listaTipoZonas": listaTipoZonas, "zona": zona,
               'nombreUsuario': request.session.get('nomreUsuario'),
               'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,
               "temperaturaok": temperaturaok, "phok": phok, "co2ok": co2ok, "humedadok":humedadok,"hayHistoria":hayHistoria}

    if request.method == 'GET':
        if not 'idUsuarioActual' in request.session:
            return redirect('loginIndex')
        if not 'idInvernadero' in request.session:
            return redirect('escogerInvernadero')
        if not tienepermiso(request, "Ver Zona"):
            return accesodenegado(request)
        if "b_ver_paneles" in request.GET:
            print('Ver Paneles de Luz')
            request.session['idZonaPanelesLuz'] = idZona
            return redirect('panelListar')


        print('Mostrar Zona Invernadero')
        ## context es el mismo de arriba
        context['editable'] = False ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Zona"):
                return accesodenegado(request)
            print('Editar Zona Invernadero')
            context['editable'] = True
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Editar Zona"):
                return accesodenegado(request)
            print('Aceptar Zona Invernadero')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idZona)
            except Exception as e:
                mensajeError = "No se puede crear la zona en este momento"
                print(e)
            try:
                zona = obtenerZonaRequest(request)
            except Exception as e:
                print(e)
                print("Error obteniendo la data del request")
                if mensajeError is not None:
                    mensajeError = "Ocurrió un error inesperado. Intente editar más tarde"

            context['zona'] = zona
            if mensajeError:
                context['editable'] = True
                context['mensajeError'] = mensajeError
                return render(request, template, context)
            else:
                hayHistoria = True
                contadorHistoria = 0
                if historiaZonaTemperatura:
                    temperaturaok = validarRangoCondiciones(historiaZonaTemperatura.temperatura, zona.temperaturamin,zona.temperaturamax)
                    contadorHistoria += 1
                else:
                    temperaturaok = None
                    hayHistoria = False

                if historiaZonaPh:
                    phok = validarRangoCondiciones(historiaZonaPh.ph, zona.phmin, zona.phmax)
                    contadorHistoria += 1
                else:
                    phok = None
                    hayHistoria = False

                if historiaZonaCo2:
                    co2ok = validarRangoCondiciones(historiaZonaCo2.concentracionco2, zona.concentracionco2min,zona.concentracionco2max)
                    contadorHistoria += 1
                else:
                    co2ok = None

                if historiaZonaHumedad:
                    humedadok = validarRangoCondiciones(historiaZonaHumedad.humedad, zona.humedadmin, zona.humedadmax)
                    contadorHistoria += 1
                else:
                    humedadok = None

                if contadorHistoria == 4:
                    hayHistoria = True

                context['editable'] = False
                context['mostrarModalEditar'] = True
                context['historiaZonaTemperatura'] = historiaZonaTemperatura
                context['historiaZonaPh'] = historiaZonaPh
                context['historiaZonaCo2'] = historiaZonaCo2
                context['historiaZonaHumedad'] = historiaZonaHumedad
                context['temperaturaok'] = temperaturaok
                context['phok'] = phok
                context['co2ok'] = co2ok
                context['humedadok'] = humedadok
                context['hayHistoria'] = hayHistoria

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Ver Zona"):
                return accesodenegado(request)
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            if not 'idUsuarioActual' in request.session:
                return redirect('loginIndex')
            if not 'idInvernadero' in request.session:
                return redirect('escogerInvernadero')
            if not tienepermiso(request, "Eliminar Zona"):
                return accesodenegado(request)
            print("Aceptar Modal")

            errorDependencia = False


            if zonaConPlanta:
                context['editable'] = False
                context['mensajeError'] = "No se puede eliminar la zona porque hay plantas asociadas"
                errorDependencia = True


            if zonaConModulo:
                context['editable'] = False
                context['mensajeError'] = "No se puede eliminar la zona porque hay módulos asociados"
                errorDependencia = True


            if zonaConPanel:
                context['editable'] = False
                context['mensajeError'] = "No se puede eliminar la zona porque hay paneles de luz asociados"
                errorDependencia = True



            if errorDependencia:
                return render(request, template, context)

            try:
                eliminarZona(request, idZona)
                request.session['mensajeZonaEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('zonaInvernaderoListar')
        else:
            return redirect('zonaInvernaderoListar')



def hayPlantasAsociadasZona(idZona):
    plantasZona = Planta.objects.filter(idzona=idZona, habilitado=True)

    if len(plantasZona) > 0:
        return True
    else:
        return False

def hayModulosAsociadasZona(idZona):
    modulosZonas = Modulosemilla.objects.filter(idzona=idZona, habilitado=True)

    if len(modulosZonas) > 0:
        return True
    else:
        return False

def hayPanelesAsociadasZona(idZona):
    panelesZonas = Panelluz.objects.filter(idzona=idZona, habilitado=True)

    if len(panelesZonas) > 0:
        return True
    else:
        return False

def eliminarZona(request,idZona):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    zona,created = Zona.objects.update_or_create(
        idzona=idZona, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    return


def obtenerZonaRequest(request):
    zonaDataLlenada = Zona()

    nombreObtenido = request.POST.get('nombre')
    codigoZonaObtenido = request.POST.get('codigoZona')
    tipoZonaEscogido = request.POST.get("tipoZona")
    area = request.POST.get('area')
    tempIdeal = request.POST.get('tempIdeal')
    tempMin = request.POST.get('tempMin')
    tempMax = request.POST.get('tempMax')

    phIdeal = request.POST.get('phIdeal')
    phMin = request.POST.get('phMin')
    phMax = request.POST.get('phMax')

    co2Ideal = request.POST.get('co2Ideal')
    co2Min = request.POST.get('co2Min')
    co2Max = request.POST.get('co2Max')

    humedadIdeal = request.POST.get('humedadIdeal')
    humedadMin = request.POST.get('humedadMin')
    humedadMax = request.POST.get('humedadMax')

    zonaDataLlenada.nombre = nombreObtenido
    zonaDataLlenada.codigozonajson = codigoZonaObtenido
    if tipoZonaEscogido != None:
        zonaDataLlenada.idtipozona = int(tipoZonaEscogido)
    zonaDataLlenada.area = area
    zonaDataLlenada.temperaturaideal = tempIdeal
    zonaDataLlenada.temperaturamin = tempMin
    zonaDataLlenada.temperaturamax = tempMax
    zonaDataLlenada.phideal = phIdeal
    zonaDataLlenada.phmin = phMin
    zonaDataLlenada.phmax = phMax
    zonaDataLlenada.concentracionco2ideal = co2Ideal
    zonaDataLlenada.concentracionco2min = co2Min
    zonaDataLlenada.concentracionco2max = co2Max
    zonaDataLlenada.humedadideal = humedadIdeal
    zonaDataLlenada.humedadmin = humedadMin
    zonaDataLlenada.humedadmax = humedadMax

    return zonaDataLlenada

def grabarData(request,idZona):
    print('GRABAR DATA')

    nombreObtenido = request.POST.get('nombre')
    codigoZonaObtenido = request.POST.get('codigoZona')
    tipoZonaEscogido = request.POST.get("tipoZona")
    area = request.POST.get('area')


    tempIdeal = request.POST.get('tempIdeal')
    if tempIdeal == "":
        tempIdeal = None

    tempMin = request.POST.get('tempMin')
    if tempMin == "":
        tempMin = None

    tempMax = request.POST.get('tempMax')
    if tempMax == "":
        tempMax = None

    phIdeal =  request.POST.get('phIdeal')
    if phIdeal == "":
        phIdeal = None

    phMin = request.POST.get('phMin')
    if phMin == "":
        phMin = None

    phMax = request.POST.get('phMax')
    if phMax == "":
        phMax = None

    co2Ideal = request.POST.get('co2Ideal')
    if co2Ideal == "":
        co2Ideal = None

    co2Min = request.POST.get('co2Min')
    if co2Min == "":
        co2Min = None

    co2Max = request.POST.get('co2Max')
    if co2Max == "":
        co2Max = None

    humedadIdeal = request.POST.get('humedadIdeal')
    if humedadIdeal == "":
        humedadIdeal = None

    humedadMin = request.POST.get('humedadMin')
    if humedadMin == "":
        humedadMin = None

    humedadMax = request.POST.get('humedadMax')
    if humedadMax == "":
        humedadMax = None

    if nombreObtenido:
        nombre = str(nombreObtenido)
        if len(nombre) > CANTIDAD_CADENA_MAXIMA:
            return "Debe ingresar un nombre menor a 250 caracteres"
    else:
        return "Falta ingresar el nombre de la zona."


    if codigoZonaObtenido:
        try:
            codigoZona = int(codigoZonaObtenido)
        except Exception as e:
            print(e)
            return "Debe ingresar un numero entero para el códido de la zona"
        if codigoZona < 0:
            return "El código de la zona debe ser mayor a cero"
    else:
        return "Falta seleccionar el codigo para la zona."

    if codigoZona == CODIGO_GENERAL_COMBO:
        return "Falta seleccionar el codigo para la zona."


    if tipoZonaEscogido:
        tipoZona = int(tipoZonaEscogido)
    else:
        return "Falta seleccionar la zona."


    if area == "":
        return "Falta ingresar el área de la zona."


    if tipoZona == ID_TIPO_ZONAS_PLANTAS:

        #
        # if tempIdeal == "":
        #     return "Falta ingresar la temperatura ideal para la zona."

        if tempMin == None:
            return "Falta ingresar la temperatura mínima para la zona."

        if tempMax == None:
            return "Falta ingresar la temperatura máxima para la zona."

        #
        # if phIdeal == "":
        #     return "Falta ingresar el PH ideal"

        if phMin == None:
            return "Falta ingresar el PH mínimo"

        if phMax == None:
            return "Falta ingresar el PH máximo"
        #
        # if co2Ideal == "":
        #     return "Falta ingresar la concentración de CO2 ideal para la zona."

        if co2Min == None:
            return "Falta ingresar la concentración de CO2 mínima para la zona."

        if co2Max == None:
            return "Falta ingresar la concentración de CO2 máxima para la zona."

        if humedadMin == None:
            return "Falta ingresar la humedad mínima para la zona."

        if humedadMax == None:
            return "Falta ingresar la humedad máxima para la zona."

    if tempMin is not None and tempMax is not None:
        tempMin = float(tempMin)
        tempMax = float(tempMax)
        if tempMin > tempMax:
            return "La temperatura mínima debe ser menor a la temperatura máxima."

    if tempIdeal is not None:
        if tempMin is None or tempMax is None:
            return "Para ingresar una temperatura ideal debe ingresar un valor mínimo y máximo"
        tempIdeal = float(tempIdeal)
        if (tempIdeal > tempMin) and (tempIdeal < tempMax):
            print("Temperatura Ideal Valida")
        else:
            return "La temperatura ideal debe ser un valor entre la mínima y la máxima."
    else:
        tempIdeal = None

    if phMin is not None and phMax is not None:
        phMin = float(phMin)
        phMax = float(phMax)
        if phMin > phMax:
            return "El pH mínimo debe ser menor al pH máximo."

    if phIdeal is not None:
        if phMin is None or phMax is None:
            return "Para ingresar una ph ideal debe ingresar un valor mínimo y máximo"
        phIdeal = float(phIdeal)
        if (phIdeal > phMin) and (phIdeal < phMax):
            print("pH Valido")
        else:
            return "El pH ideal debe ser un valor entre el mínimo y el máximo."
    else:
        phIdeal = None

    if co2Min is not None and co2Max is not None:
        co2Min = float(co2Min)
        co2Max = float(co2Max)
        if co2Min > co2Max:
            return "La concentración de CO2 mínima debe ser mayor a la concentración de CO2 máxima."


    if co2Ideal is not None:
        if co2Min is None or co2Max is None:
            return "Para ingresar una concentración de CO2 ideal debe ingresar un valor mínimo y máximo"
        co2Ideal = float(co2Ideal)
        if (co2Ideal > co2Min) and (co2Ideal < co2Max):
            print("CO2 Valido")
        else:
            return "El CO2 ideal debe ser un valor entre el mínimo y el máximo."
    else:
        co2Ideal = None

    if humedadMin is not None and humedadMax is not None:
        humedadMin = float(humedadMin)
        humedadMax = float(humedadMax)
        if humedadMin > humedadMax:
            return "La humedad mínima debe ser mayor a la humedad máxima."

    if humedadIdeal is not None:
        if humedadMin is None or humedadMax is None:
            return "Para ingresar una humedad ideal debe ingresar un valor mínimo y máximo"
        humedadIdeal = float(humedadIdeal)
        if (humedadIdeal > humedadMin) and (humedadIdeal < humedadMax):
            print("Humedad Válida")
        else:
            return "La humedad ideal debe ser un valor entre el mínimo y el máximo."
    else:
        humedadIdeal = None



    idInvernaderoObtenido =  request.session.get('idInvernadero')
    if idInvernaderoObtenido == "" or idInvernaderoObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."

    idInvernadero = int(idInvernaderoObtenido)

    idUsuarioObtenido = request.session.get('idUsuarioActual')
    if idUsuarioObtenido == "" or idUsuarioObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."
    idUsuarioActual = int(idUsuarioObtenido)

    # print('Nombre: ' + str(nombre))
    # print('Codigo Zona: ' + str(codigoZona))
    # print('Tipo Zona:' + str(tipoZona))
    # print('area: ' + str(area))
    # print('tempIdeal: ' + str(tempIdeal))
    # print('tempMin: ' + str(tempMin))
    # print('tempMax: ' + str(tempMax))
    # print('co2Ideal: ' + str(co2Ideal))
    # print('co2Min: ' + str(co2Min))
    # print('co2Max: ' + str(co2Max))
    # print('Id Invernadero: ' + str(idInvernadero))
    # print('Id Usuario Actual: ' + str(idUsuarioActual))

    zonaObtenidaBd = None
    if idZona is None:
        idMax = Zona.objects.all().aggregate(Max('idzona'))['idzona__max']
        if idMax is None:
            idZona = 1
        else:
            idZona = idMax + 1
        zonaObtenidaBd = Zona.objects.filter(codigozonajson=codigoZona, habilitado=True)

    else:
        zonaObtenidaBd = Zona.objects.filter(codigozonajson=codigoZona, habilitado=True).exclude(idzona=idZona)
        print(zonaObtenidaBd)
    if zonaObtenidaBd.exists():
        return "Ya existe el codigo de zona. Ingrese un codigo de zona distinto"

    with transaction.atomic():
        zona,created = Zona.objects.update_or_create(
            idzona=idZona, defaults={ "idtipozona" :tipoZona,
            "idinvernadero" : idInvernadero,
            "codigozonajson": codigoZona,
            "nombre" : nombre,
            "area" :area,
            "temperaturaideal":tempIdeal,
            "temperaturamin" :tempMin,
            "temperaturamax" :tempMax,
            "phideal": phIdeal,
            "phmin": phMin,
            "phmax": phMax,
            "concentracionco2ideal":co2Ideal,
            "concentracionco2min":co2Min,
            "concentracionco2max":co2Max,
            "humedadideal":humedadIdeal,
            "humedadmin":humedadMin,
            "humedadmax":humedadMax,
            "fechacreacion" :datetime.now(),
            "habilitado":True,
            "idusuarioauditado": idUsuarioActual}
        )


    return None


