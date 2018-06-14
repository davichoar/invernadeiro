from app.models import Historiainvernadero, Historiamodulo, Historiapanel, Historiaplanta
from app.models import Historiasemilla, Historiazona
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def prueba(request, template=None, extra_context=None):
    if request.method == 'GET':
        content = 'prueba del cliente'
        print('prueba del servidor')
        return HttpResponse(content, content_type='text/plain')
    if request.method == 'POST':
        cadena = request.body.decode('utf-8')
        print(cadena)
        return HttpResponse('recibi tu mensaje', content_type='text/plain')
