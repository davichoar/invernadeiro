from app.models import Zona, Historiazona, Planta, Historiaplanta, Modulosemilla, Historiamodulo, Tipoplanta
from django.http import JsonResponse

def _getSeedsModulesStats(id_zone):
    modules = Modulosemilla.objects.filter(idzona=id_zone, habilitado = True).values()
    modules_arr = list(modules)

    for module in modules_arr:
        stats = Historiamodulo.objects.all().filter(idmodulo=module['idmodulo']).order_by('fecharegistro')[:10].values()
        stats_arr = list(stats)

        module['fecharegistro'] = []
        module['temperatura'] = []
        module['humedadtierra'] = []
        module['humedadambiente'] = []
        module['nivelagua'] = []
        module['concentracionco2'] = []
        module['luz'] = []

        for item in stats_arr:
            module['fecharegistro'].append(item['fecharegistro'].strftime('%d/%m %H:%M'))
            module['temperatura'].append(item['temperatura'])
            module['humedadtierra'].append(item['humedadtierra'])
            module['humedadambiente'].append(item['humedadambiente'])
            module['nivelagua'].append(item['nivelagua'])
            module['concentracionco2'].append(item['concentracionco2'])
            module['luz'].append(item['luz'])

    return modules_arr

def _getPlantsStats(id_zone):
    plants = Planta.objects.filter(idzona=id_zone, habilitado = True).values()
    plants_arr = list(plants)

    for plant in plants_arr:
        plant_type = Tipoplanta.objects.all().filter(idtipoplanta=plant['idtipoplanta']).values('nombrecomun')
        plant['nombrecomun'] = list(plant_type)[0]['nombrecomun']
        stats = Historiaplanta.objects.all().filter(idplanta=plant['idplanta']).order_by('fecharegistro')[:10].values()
        stats_arr = list(stats)

        plant['fecharegistro'] = []
        plant['humedad'] = []

        for item in stats_arr:            
            plant['fecharegistro'].append(item['fecharegistro'].strftime('%d/%m %H:%M'))
            plant['humedad'].append(item['humedad'])
    
    return plants_arr

def zone_stats(request):
    idinvernadero = request.session['idInvernadero']
    id_zone = request.GET.get('idzona')

    if (id_zone is None):
        return JsonResponse({}, safe=False)

    zone = Zona.objects.all().filter(pk=id_zone, idinvernadero=idinvernadero).values()
    zone_dict = list(zone)[0]
    zone_dict['fecharegistro'] = []
    zone_dict['temperatura'] = []
    zone_dict['ph'] = []
    zone_dict['concentracionco2'] = []

    stats = Historiazona.objects.all().filter(idzona=id_zone).order_by('fecharegistro')[:10].values()
    stats_arr = list(stats)

    for item in stats_arr:
        zone_dict['fecharegistro'].append(item['fecharegistro'].strftime('%d/%m %H:%M'))
        zone_dict['temperatura'].append(item['temperatura'])
        zone_dict['ph'].append(item['ph'])
        zone_dict['concentracionco2'].append(item['concentracionco2'])

    if (zone_dict['idtipozona'] == 1):
        zone_dict['modules'] = _getSeedsModulesStats(id_zone)
    elif (zone_dict['idtipozona'] == 2):
        zone_dict['plants'] = _getPlantsStats(id_zone)

    return JsonResponse(zone_dict, safe=False)