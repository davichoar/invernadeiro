from django.shortcuts import render
from app.models import Historiainvernadero
import json

def index(request):
    template = 'app/estadisticas/index.html'
    idInvernadero = request.session['idInvernadero']
    data = Historiainvernadero.objects.order_by('fecharegistro')[:10]
    context= {
        'labels_5': json.dumps([x.fecharegistro.strftime('%d/%m') for x in data[:5]]),
        'energy_5': [x.nivelenergia for x in data[:5]],
        'water_5': [x.niveltanqueagua for x in data[:5]],
        'labels_10': [x.fecharegistro.strftime('%d/%m') for x in data],
        'energy_10': [x.nivelenergia for x in data],
        'water_10': [x.niveltanqueagua for x in data]
    }
    return render(request, template, context)