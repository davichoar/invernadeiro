from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime
from django.template import loader
from django.urls import reverse

from app.models import Usuario, Invernadero, Usuarioxinvernadero, Zona, Tipozona, Historiainvernadero, Historiazona


def crear(request,
          template='app/zonainvernadero/create.html',
          extra_context=None):
    if request.method == 'GET':
        print('CREAR ZONAS DEL INVERANDERO')
        listaTipoZonas = Tipozona.objects.filter(habilitado = True)
        context = {"listaTipoZonas": listaTipoZonas,
                   'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),
                   }
        return render(request, template, context)
    elif request.method == 'POST':

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
                zona = obtenerZonaRequest(request)
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
    #template = loader.get_template('app/zonainvernadero/list.html')
    template = "app/zonainvernadero/list.html"
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


        mensajeCreacion = request.session.pop('mensajeZonaCrear',False)
        mensajeEliminar = request.session.pop('mensajeZonaEliminar', False)

        print(listaZonas)
        context = {"historia":ultimaHistoria,"listaZonas": listaZonas.order_by('idzona'), 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('zonaInvernaderoCrear')
    context = {}
    return render(request, template, context)


def detalle(request,idZona):

    template = 'app/zonainvernadero/show.html'
    zona = Zona.objects.get(idzona=idZona)
    listaTipoZonas = Tipozona.objects.filter(habilitado=True)

    try:
        historiaZona = Historiazona.objects.filter(idzona=idZona).order_by('-fecharegistro')[0]
    except Exception as e:
        historiaZona = None
        print(e)

    if request.method == 'GET':
        print('Mostrar Zona Invernadero')
        context = {"historiaZona":historiaZona,"listaTipoZonas":listaTipoZonas,"zona": zona, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'), "editable":False,}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            print('Editar Zona Invernadero')
            context = {"historiaZona":historiaZona,"listaTipoZonas":listaTipoZonas,"zona": zona, 'nombreUsuario': request.session.get('nomreUsuario'),
                       'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": True, }
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
                           'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": True, "mensajeError":mensajeError}
                return render(request, template, context)
            else:
                return redirect('zonaInvernaderoListar')

        if "b_cancelar" in request.POST :
            context = {"historiaZona": historiaZona, "listaTipoZonas": listaTipoZonas, "zona": zona,
                       'nombreUsuario': request.session.get('nomreUsuario'),
                       'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False, }
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


def obtenerZonaRequest(request):
    zonaDataLlenada = Zona()

    nombreObtenido = request.POST.get('nombre')
    codigoZonaObtenido = request.POST.get('codigoZona')
    tipoZonaEscogido = request.POST.get("tipoZona")
    area = request.POST.get('area')
    tempIdeal = request.POST.get('tempIdeal')
    tempMin = request.POST.get('tempMin')
    tempMax = request.POST.get('tempMax')
    co2Ideal = request.POST.get('co2Ideal')
    co2Min = request.POST.get('co2Min')
    co2Max = request.POST.get('co2Max')

    zonaDataLlenada.nombre = nombreObtenido
    zonaDataLlenada.codigozonajson = codigoZonaObtenido
    zonaDataLlenada.idtipozona = tipoZonaEscogido
    zonaDataLlenada.area = area
    zonaDataLlenada.temperaturaideal = tempIdeal
    zonaDataLlenada.temperaturamin = tempMin
    zonaDataLlenada.temperaturamax = tempMax
    zonaDataLlenada.concentracionco2ideal = co2Ideal
    zonaDataLlenada.concentracionco2min = co2Min
    zonaDataLlenada.concentracionco2max = co2Max
    return zonaDataLlenada

def grabarData(request,idZona):
    print('GRABAR DATA')

    nombreObtenido = request.POST.get('nombre')
    codigoZonaObtenido = request.POST.get('codigoZona')
    tipoZonaEscogido = request.POST.get("tipoZona")
    area = request.POST.get('area')
    tempIdeal = request.POST.get('tempIdeal')
    tempMin = request.POST.get('tempMin')
    tempMax = request.POST.get('tempMax')
    co2Ideal = request.POST.get('co2Ideal')
    co2Min = request.POST.get('co2Min')
    co2Max = request.POST.get('co2Max')

    if nombreObtenido:
        nombre = str(nombreObtenido)
    else:
        return "Falta ingresar el nombre de la zona."


    if codigoZonaObtenido:
        codigoZona = int(codigoZonaObtenido)
    else:
        return "Falta ingresar el codigo para la zona."


    if tipoZonaEscogido:
        tipoZona = int(tipoZonaEscogido)
    else:
        return "Falta seleccionar la zona."


    if area == "":
        return "Falta ingresar el área de la zona."


    if tempIdeal == "":
        return "Falta ingresar la temperatura ideal para la zona."


    if tempMin == "":
        return "Falta ingresar la temperatura mínima para la zona."


    if tempMax == "":
        return "Falta ingresar la temperatura máxima para la zona."


    if co2Ideal == "":
        return "Falta ingresar la concentración de CO2 ideal para la zona."


    if co2Min == "":
        return "Falta ingresar la concentración de CO2 mínima para la zona."


    if co2Max == "":
        return "Falta ingresar la concentración de CO2 máxima para la zona."

    idInvernaderoObtenido =  request.session.get('idInvernadero')
    if idInvernaderoObtenido == "" or idInvernaderoObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."

    idInvernadero = int(idInvernaderoObtenido)

    idUsuarioObtenido = request.session.get('idUsuarioActual')
    if idUsuarioObtenido == "" or idUsuarioObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."
    idUsuarioActual = int(idUsuarioObtenido)

    print('Nombre: ' + nombre)
    print('Codigo Zona: ' + str(codigoZona))
    print('Tipo Zona:' + str(tipoZona))
    print('area: ' + area)
    print('tempIdeal: ' + tempIdeal)
    print('tempMin: ' + tempMin)
    print('tempMax: ' + tempMax)
    print('co2Ideal: ' + co2Ideal)
    print('co2Min: ' + co2Min)
    print('co2Max: ' + co2Max)
    print('Id Invernadero: ' + str(idInvernadero))
    print('Id Usuario Actual: ' + str(idUsuarioActual))

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


    zona,created = Zona.objects.update_or_create(
        idzona=idZona, defaults={ "idtipozona" :tipoZona,
        "idinvernadero" : idInvernadero,
        "codigozonajson": codigoZona,
        "nombre" : nombre,
        "area" :area,
        "temperaturaideal":tempIdeal,
        "temperaturamin" :tempMin,
        "temperaturamax" :tempMax,
        "concentracionco2ideal":co2Ideal,
        "concentracionco2min":co2Min,
        "concentracionco2max":co2Max,
        "fechacreacion" :datetime.now(),
        "habilitado":True,
        "idusuarioauditado":idUsuarioActual}
    )

    zona.save()

    return None


