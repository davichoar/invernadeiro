from django.shortcuts import render
from app.models import Historiainvernadero, Zona
import json

def stats_all(request):
    template = 'app/estadisticas/index.html'
    idInvernadero = request.session['idInvernadero']
    stats_invernadero = Historiainvernadero.objects.filter(idinvernadero=idInvernadero).order_by('fecharegistro')[:10]
    zones = Zona.objects.all().filter(idinvernadero=idInvernadero).order_by('idzona')
    context= {
        'labels': [x.fecharegistro.strftime('%d/%m') for x in stats_invernadero],
        'energy': [x.nivelenergia for x in stats_invernadero],
        'water': [x.niveltanqueagua for x in stats_invernadero],
        'zones': [{'idzona': x.idzona, 'nombre': x.nombre}  for x in zones]
    }
    return render(request, template, context)