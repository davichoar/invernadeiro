from django.db.models import Max
from django.shortcuts import render, redirect
from datetime import datetime

from app.models import Usuario, Invernadero, Usuarioxinvernadero, Zona


def crear(request,
          template='app/zonainvernadero/create.html',
          extra_context=None):
    if request.method == 'GET':
        print('CREAR INVERANDERO')
        context = {}
        return render(request, template, context)
    elif request.method == 'POST':

        if "b_aceptar" in request.POST:

            print('GRABAR DATA')
            nombre = str (request.POST.get('nombre'))
            codigoZona = request.POST.get('codigoZona')
            area = request.POST.get('area')
            tempIdeal = request.POST.get('tempIdeal')
            tempMin = request.POST.get('tempMin')
            tempMax = request.POST.get('tempMax')
            co2Ideal = request.POST.get('co2Ideal')
            co2Min = request.POST.get('co2Min')
            co2Max = request.POST.get('co2Max')

            print('Nombre: ' + nombre)
            print('Codigo Zona: '+codigoZona)
            print('area: ' + area)
            print('tempIdeal: ' + tempIdeal)
            print('tempMin: ' + tempMin)
            print('tempMax: ' + tempMax)
            print('co2Ideal: ' + co2Ideal)
            print('co2Min: ' + co2Min)
            print('co2Max: ' + co2Max)
            nuevoid = Zona.objects.all().aggregate(Max('idzona'))['idzona__max'] + 1
            zona = Zona.objects.create(
                idzona = nuevoid,
                idtipozona = 1,
                idinvernadero = request.session.get('idInvernadero'),
                codigozona = codigoZona,
                nombre = nombre,
                area = area,
                temperaturaideal = tempIdeal,
                temperaturamin = tempMin,
                temperaturamax = tempMax,
                fechacreacion = datetime.now(),
                habilitado=True,
                idusuarioauditado = request.session.get('idUsuarioActual')
            )

            zona.save()


        return redirect('index', idInvernadero=request.session.get('idInvernadero'))
    else:
        return

