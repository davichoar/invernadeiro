from django.shortcuts import render
from app.models import Historiainvernadero, Zona, Modulosemilla, Planta, Tipoplanta
import json

def stats_all(request):
    template = 'app/estadisticas/index.html'
    idInvernadero = request.session['idInvernadero']
    stats_invernadero = Historiainvernadero.objects.filter(idinvernadero=idInvernadero).order_by('fecharegistro')[:10]
    zones = Zona.objects.filter(idinvernadero=idInvernadero, habilitado=True).order_by('idzona')
    context= {
        'labels': [x.fecharegistro.strftime('%d/%m/%Y') for x in stats_invernadero],
        'fechasstr': [x.fecharegistro.strftime('%Y/%m/%d/%H/%M/%S') for x in stats_invernadero],
        'energy': [x.nivelenergia for x in stats_invernadero],
        'water': [x.niveltanqueagua for x in stats_invernadero],
        'zones': [{'idzona': x.idzona, 'nombre': x.nombre}  for x in zones], 
        'nombreUsuario': request.session.get('nomreUsuario'),
        'nombreInvernadero': request.session.get('nombreInvernadero'),
    }
    return render(request, template, context)

def expanded_stats(request):
    template = 'app/estadisticas/detalle.html'
    obj_type = request.GET.get('type')
    obj_id = request.GET.get('id')
    param = request.GET.get('param')
    idInvernadero = request.session['idInvernadero']
    obj_info = _get_obj_info(idInvernadero, obj_type, obj_id, param)
    print(obj_info)
    context = {
        'obj_name': obj_info['name'],
        'obj_param': obj_info['param'],
        'api_url': obj_info['api_url'], 
        'nombreUsuario': request.session.get('nomreUsuario'),
        'nombreInvernadero': request.session.get('nombreInvernadero'),
    }
    return render(request, template, context)

def _get_obj_info(inv, obj_type, obj_id, param):
    obj_dict = {
        'name': None,
        'param': None,
        'api_url': None
    }

    if obj_type == 'zona':
        obj_dict['name'] = Zona.objects.get(idzona=obj_id).nombre
        obj_dict['api_url'] = '../../api/historiazona/'
    elif obj_type == 'modulo':
        obj_dict['name'] = Modulosemilla.objects.get(idmodulo=obj_id).nombre
        obj_dict['api_url'] = '../../api/historiamodulo/'
    elif obj_type == 'planta':
        idtipoplanta = Planta.objects.get(idplanta=obj_id).idtipoplanta
        obj_dict['name'] = Tipoplanta.objects.get(idtipoplanta=idtipoplanta).nombrecomun
        obj_dict['api_url'] = '../../api/historiaplanta/'
    else:
        return None

    # Mapping of the value of the buttons and its corresponding parameter
    params = {
        'temp': 'Temperatura',
        'ph': 'pH',
        'co2': 'CO2',
        'hum_tie': 'Humedad en tierra',
        'hum_amb': 'Humedad en el ambiente',
        'agua': 'Nivel de agua'        
    }

    obj_dict['param'] = params[param]
    return obj_dict