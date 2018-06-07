from django.db.models import Max
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime

from app.models import Zona, Tipozona, Historiainvernadero, Historiazona, Modulosemilla, Historiamodulo, Tipoplanta, \
    Planta, Semilla, Historiaplanta, Panelluz, Historiapanel

ID_TIPO_ZONAS_PLANTAS = 2
ID_TODAS_ZONAS = -1
def crear(request,
          template='app/panelluz/crear.html',
          extra_context=None):

    try:
        idInvernadero = int(request.session.get('idInvernadero'))
        listaZonas = Zona.objects.filter(idinvernadero=idInvernadero, idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePanelCrearError'] = True
        return redirect('panelListar')

    if request.method == 'GET':
        print('CREAR PANELES')
        context = {'listaZonas':listaZonas,
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
                mensajeError = "No se puede crear el panel de luz en este momento"
                print(e)

            if mensajeError is not None:
                print("MENSAJE ERROR CREAR ZONA")
                panel = obtenerPanelRequest(request)
                context = {"planta":panel,
                           'listaZonas': listaZonas,
                           'nombreUsuario': request.session.get('nomreUsuario'),
                           'nombreInvernadero': request.session.get('nombreInvernadero'),
                           'mensajeError': mensajeError,
                           }
                return render(request, template, context)
            else:
                request.session['mensajePanelCrear'] = True
        return redirect('panelListar')
    else:
        return redirect('panelListar')


def listar(request,
          extra_context=None):
    #template = loader.get_template('app/zonainvernadero/lista.html')
    template = "app/panelluz/lista.html"
    listaPaneles = []
    if request.method == 'GET':

        print('LISTAR PANELES')
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
        mensajePanelCrearEditarError = False

        if listaIdZonas != None:
            if "b_buscar" in request.GET:
                valorBusqueda = request.GET.get('textoBusqueda')
                print(valorBusqueda)
                if (valorBusqueda is None):
                    valorBusqueda = ""
                try:
                    listaPaneles = Panelluz.objects.filter(codigopaneljson__icontains = valorBusqueda,idzona__in = listaIdZonas, habilitado=True)
                except Exception as e:
                    print(e)
                    listaPaneles = None
            else:
                try:
                    listaPaneles = Panelluz.objects.filter(idzona__in = listaIdZonas,habilitado=True)
                except Exception as e:
                    print(e)
                    listaPaneles = None

            mensajeCreacion = request.session.pop('mensajePanelCrear', False)
            mensajeEliminar = request.session.pop('mensajePanelEliminar', False)
            mensajePanelCrearEditarError = request.session.pop('mensajePanelCrearEditarError', False)

            if listaPaneles:
                listaPaneles = listaPaneles.order_by('idpanel')

        else:
            mensajeObtenerZonaError = True
            zonaSeleccionada = ID_TODAS_ZONAS

        print('Lista de paneles')
        print(listaPaneles)
        print(zonaSeleccionada)
        if zonaSeleccionada != None:
            zonaSeleccionada = int(zonaSeleccionada)
        context = {"idseleccionado":zonaSeleccionada,"listaZonas":listaZonas,"listaPaneles": listaPaneles, 'nombreUsuario': request.session.get('nomreUsuario'),
                   'nombreInvernadero': request.session.get('nombreInvernadero'),"mensajeCreacion": mensajeCreacion,"mensajeEliminacion": mensajeEliminar,"mensajePanelCrearEditarError":mensajePanelCrearEditarError,"mensajeObtenerZonaError":mensajeObtenerZonaError}
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_crear" in request.POST:
            return redirect('panelCrear')
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


def detalle(request,idPanel):

    template = 'app/panelluz/verEditar.html'
    panel = Panelluz.objects.get(idpanel=idPanel)

    try:
        idInvernadero = int(request.session.get('idInvernadero'))
        listaZonas = Zona.objects.filter(idinvernadero=idInvernadero, idtipozona=ID_TIPO_ZONAS_PLANTAS, habilitado=True)
    except Exception as e:
        print(e)
        request.session['mensajePanelCrearEditarError'] = True
        return redirect('panelListar')


    try:
        historiaPanel = Historiapanel.objects.filter(idpanel=idPanel).order_by('-fecharegistro')[0]
    except Exception as e:
        historiaPanel = None
        print(e)

    context = {"historiaPanel": historiaPanel,"listaZonas": listaZonas, "panel": panel,
               'nombreUsuario': request.session.get('nomreUsuario'),
               'nombreInvernadero': request.session.get('nombreInvernadero'), "editable": False,}

    if request.method == 'GET':
        print('Mostrar Panel')
        ## context es el mismo de arriba
        context['editable'] = False ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
        return render(request, template, context)

    elif request.method == 'POST':
        if "b_editar" in request.POST:
            print('Editar Panel')
            context['editable'] = True
            return render(request, template, context)
        if "b_aceptar" in request.POST:
            print('Aceptar Panel')
            mensajeError = None
            try:
               mensajeError = grabarData(request,idPanel)
            except Exception as e:
                mensajeError = "No se puede crear el panel de luz en este momento"
                print(e)
            panel = obtenerPanelRequest(request)
            context['panel'] = panel
            if mensajeError:

                context['editable'] = True
                context['mensajeError'] = mensajeError

                return render(request, template, context)
            else:

                context['editable'] = False
                context['mostrarModalEditar'] = True

                return render(request, template, context)

        if "b_cancelar" in request.POST :
            ## context es el mismo de arriba
            context['editable'] = False  ## es un saludo a la bandera, solo para aclarar que la vista no sera editable
            return render(request, template, context)
        if "b_aceptar_modal" in request.POST:
            print("Aceptar Modal")
            try:
                eliminarPanel(request, idPanel)
                request.session['mensajePanelEliminar'] = True
            except Exception as e:
                print(e)

            return redirect('panelListar')
        else:
            return redirect('panelListar')

def eliminarPanel(request,idPanel):
    idUsuarioActual = int(request.session.get('idUsuarioActual'))
    panel,created = Panelluz.objects.update_or_create(
        idpanel=idPanel, defaults={"habilitado":False,"idusuarioauditado":idUsuarioActual})
    print(created)
    panel.save()
    return


def obtenerPanelRequest(request):
    panelLuz = Panelluz()

    idzona = request.POST.get('zona')
    codigoPanel = request.POST.get('codigoPanel')

    panelLuz.idzona = idzona
    panelLuz.codigopaneljson = codigoPanel

    return panelLuz

def grabarData(request,idPanel):
    print('GRABAR DATA')

    idzona = request.POST.get('zona')
    codigoPanel = request.POST.get('codigoPanel')

    if idzona:
        idzona = int(idzona)
    else:
        return "Falta seleccionar la zona para el panel de luz"


    if codigoPanel == "":
        return "Falta ingresar el código para el panel de luz."
    else:
        try:
            codigoPanel = int(codigoPanel)
        except Exception as e:
            print(e)
            return "Debe ingresar un numero entero para el código del panel de luz"
        if codigoPanel < 0:
            return "El código de panel de luz debe ser mayor a cero"


    idUsuarioObtenido = request.session.get('idUsuarioActual')
    if idUsuarioObtenido == "" or idUsuarioObtenido == None:
        return "Ocurrió un error al tratar de crear la zona. Intente de nuevo en un momento."
    idUsuarioActual = int(idUsuarioObtenido)

    panelObtenidoBd = None
    if idPanel is None:
        idMax = Panelluz.objects.all().aggregate(Max('idpanel'))['idpanel__max']
        if idMax is None:
            idPanel = 1
        else:
            idPanel = idMax + 1
        panelObtenidoBd = Panelluz.objects.filter(codigopaneljson=codigoPanel, habilitado=True)

    else:
        panelObtenidoBd = Panelluz.objects.filter(codigopaneljson=codigoPanel, habilitado=True).exclude(idpanel=idPanel)
        print(panelObtenidoBd)
    if panelObtenidoBd.exists():
        return "Ya existe el codigo del panel de luz. Ingrese un codigo de panel distinto"

    panel,created = Panelluz.objects.update_or_create(
        idpanel=idPanel, defaults={
        "idzona":idzona,
        "codigopaneljson" :codigoPanel,
        "fechacreacion":datetime.now(),
        "habilitado":True,
        "idusuarioauditado":idUsuarioActual}
    )

    panel.save()

    return None

