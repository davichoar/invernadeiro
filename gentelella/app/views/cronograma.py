from django.core.serializers import json, serialize
from rest_framework.renderers import JSONRenderer

from app.models import Historiainvernadero, Historiamodulo, Historiapanel, Historiaplanta, Cronograma, Invernadero, \
    Zona, Modulosemilla
from app.models import Historiazona, Foto
from datetime import datetime
from django.db.models import Max
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers

class CronogramaSerializer(serializers.Serializer):
    horainicio = serializers.IntegerField()
    horafin = serializers.IntegerField()
    temperatura = serializers.FloatField()
    humedadambiente = serializers.FloatField()
    humedadtierra = serializers.FloatField()
    concentracionco2 = serializers.FloatField()
    luz = serializers.BooleanField()
    nivelagua = serializers.FloatField()

@csrf_exempt
def obtener(request, template=None, extra_context=None):

    if request.method == 'GET':
        print(request.GET)
        try:
            codigoInvernadero = request.GET['codigoInvernadero']
            codigoZona = request.GET['codigoZona']
            codigoModulo = request.GET['codigoModulo']
        except Exception as e:
            print("Falta algun parametro")
            print(e)

        codigoInvernadero = int (codigoInvernadero)
        codigoZona = int (codigoZona)
        codigoModulo = int (codigoModulo)

        listaInvernadero = Invernadero.objects.filter(codigoinvernaderojson=codigoInvernadero)
        print("Lista de Invernadero")
        print(listaInvernadero)
        if listaInvernadero is not None and ( len(listaInvernadero) > 0):
            zona = None
            for invernadero in listaInvernadero:
                zona = Zona.objects.get(idinvernadero = invernadero.idinvernadero,codigozonajson = codigoZona)
                if zona:
                    break
            if zona:
                print("Zona")
                print(zona)
                modulo = Modulosemilla.objects.get(idzona=zona.idzona,codigomodulojson=codigoModulo)
            else:
                print("No se encontro ninguna zona para los datos enviados")

            print("Modulo")
            print(modulo)

            listaRegistrosCronograma = Cronograma.objects.filter(idmodulo=modulo.idmodulo)
            print("Cronograma")
            cronogramaSerializado = CronogramaSerializer(listaRegistrosCronograma,many=True)
            jasonCronograma = JSONRenderer().render(cronogramaSerializado.data)
            print(jasonCronograma)

        return HttpResponse(jasonCronograma, content_type='text/plain')

    return HttpResponse("Debe ser un metodo GET", content_type='text/plain')