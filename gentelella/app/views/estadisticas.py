from django.shortcuts import render
from app.models import Historiainvernadero, Zona
import json

def index(request):
    template = 'app/estadisticas/index.html'
    idInvernadero = request.session['idInvernadero']
    stats_invernadero = Historiainvernadero.objects.filter(idinvernadero=idInvernadero).order_by('fecharegistro')[:10]
    zonas = Zona.objects.all().filter(idinvernadero=idInvernadero)
    context= {
        'labels': [x.fecharegistro.strftime('%d/%m') for x in stats_invernadero],
        'energy': [x.nivelenergia for x in stats_invernadero],
        'water': [x.niveltanqueagua for x in stats_invernadero],
    }
    print(idInvernadero, zonas)
    return render(request, template, context)