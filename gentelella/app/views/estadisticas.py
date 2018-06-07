from django.shortcuts import render
from app.models import Historiainvernadero
import json

def index(request):
    template = 'app/estadisticas/index.html'
    idInvernadero = request.session['idInvernadero']
    data = Historiainvernadero.objects.order_by('fecharegistro')[:10]
    context= {
        'labels': [x.fecharegistro.strftime('%d/%m') for x in data],
        'energy': [x.nivelenergia for x in data],
        'water': [x.niveltanqueagua for x in data],
    }
    return render(request, template, context)