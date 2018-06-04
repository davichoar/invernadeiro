from app.models import Historiainvernadero, Historiamodulo, Historiapanel, Historiaplanta
from app.models import Historiazona, Foto
from datetime import datetime
from django.db.models import Max
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import base64
import os

rutaDefault='/app/static/received_images/'
formatoDefault='.jpg'
#rutaProyecto='/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])
rutaProyecto=settings.BASE_DIR
rutaFinal=os.path.join(rutaProyecto,rutaDefault)


def selectID(actual_id):
    if actual_id is None:
        return 0
    else:
        return actual_id

@csrf_exempt
def prueba(request, template=None, extra_context=None):
    global rutaFinal
    global formatoDefault
    if request.method == 'GET':
        #rechicken
        content = 'prueba del servidor'
        print('prueba del servidor')
        return HttpResponse(content, content_type='text/plain')
    if request.method == 'POST':
        jsonATomar  = json.loads(request.body)
        if jsonATomar['tipoJson'] == 0: #Foto
        	
            for jsonFoto in jsonATomar['listaFotos']:
                nuevoid = selectID(Foto.objects.all().aggregate(Max('idfoto'))['idfoto__max']) + 1

                nombreArch = str(jsonFoto['codigoModulo']) + '_' + str(nuevoid)
                rutaArchivo = os.path.join(rutaFinal,nombreArch+formatoDefault)
                #Guardando en la carpeta

                #imagenCont = base64.b64decode(jsonFoto['foto'])
                #with open(rutaArchivo, 'wb') as f:
                #    f.write(imagenCont)
                

                #Guardando en la base de datos.
                
                nuevaFoto = Foto.objects.create(
                    idfoto = nuevoid,
                    idmodulo = int(jsonFoto['codigoModulo']),
                    ruta = rutaArchivo,
                    nombresinextension = nombreArch,
                    extension = formatoDefault,
                    nombrefoto = 'semilla_' + str(nuevoid), #nombre inicial
	                fecharegistro = datetime.now() #maybe a corregir.
                )

                


        elif jsonATomar['tipoJson'] == 1: #modulo semillero
        	
            for jsonModulo in jsonATomar['listaModulos']:
                nuevoid = selectID(Historiamodulo.objects.all().aggregate(Max('idhistoriamodulo'))['idhistoriamodulo__max']) + 1
                nuevaHModulo = Historiamodulo.objects.create(
                    idhistoriamodulo = nuevoid,
                    idmodulo = int(jsonModulo['codigoModulo']),
                    temperatura = float(jsonModulo['temperatura']),
                    humedadtierra = float(jsonModulo['humedadTierra']),
                    humedadambiente = float(jsonModulo['humedadAmbiente']),
                    nivelagua= float(jsonModulo['nivelAgua']),
                    concentracionco2= float(jsonModulo['concentracionCO2']),
                    luz= jsonModulo['luz'], ##no me convence lol
                    fecharegistro = datetime.now(), #maybe a corregir.
                    comentario = 'meme'
                )

        elif jsonATomar['tipoJson'] == 2:
            nuevoid = selectID(Historiazona.objects.all().aggregate(Max('idhistoriazona'))['idhistoriazona__max']) + 1
            nuevaHZona = Historiazona.objects.create(
                idhistoriazona = nuevoid,
                idzona = int(jsonATomar['codigoZona']),
                temperatura = float(jsonATomar['temperaturaZona']),
                ph = float(jsonATomar['phZona']),
                concentracionco2 = float(jsonATomar['concentracionCO2']),
                fecharegistro= datetime.now()
            )
            for jsonPlanta in jsonATomar['listaPlantas']:
                nuevoplantaid = selectID(Historiaplanta.objects.all().aggregate(Max('idhistoriaplanta'))['idhistoriaplanta__max']) + 1
                nuevaHPlanta = Historiaplanta.objects.create(
                    idhistoriaplanta = nuevoplantaid,
                    idplanta = int(jsonPlanta['codigoPlanta']),
                    idzona = int(jsonATomar['codigoZona']),
                    humedad = float(jsonPlanta['humedadPlanta']),
                    fecharegistro= datetime.now(), #to change
                    comentario='meme'
                )
            for jsonPanel in jsonATomar['listaPanelesLuz']:
                nuevopanelid = selectID(Historiapanel.objects.all().aggregate(Max('idhistoriapanel'))['idhistoriapanel__max']) + 1
                nuevoHPanel = Historiapanel.objects.create(
                    idhistoriapanel = nuevopanelid,
                    idpanel = int(jsonPanel['codigoPanel']),
                    encendido = jsonPanel['encendido'],
                    fecharegistro= datetime.now() #tochange
                )



        elif jsonATomar['tipoJson'] == 3: #invernadero general
            nuevoid = selectID(Historiainvernadero.objects.all().aggregate(Max('idhistoriainvernadero'))['idhistoriainvernadero__max']) + 1
            nuevaHInvernadero = Historiainvernadero.objects.create(
                idhistoriainvernadero = nuevoid,
                idinvernadero = int(jsonATomar['codigoInvernadero']),
                nivelenergia = float(jsonATomar['energia']),
                niveltanqueagua = float(jsonATomar['nivelTanque']),
                comentario = 'meme',
                fecharegistro= datetime.now()
            )
        return HttpResponse('nice', content_type='text/plain')
