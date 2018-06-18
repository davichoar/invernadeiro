from app.models import Zona, Modulosemilla, Historiamodulo
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def get(request):    
    try:
        idmodulo = request.GET.get('id')
        idzona = Modulosemilla.objects.get(idmodulo=id).idzona
        idinvernadero = request.session['idInvernadero']
        modulo = Zona.objects.get(idinvernadero=idinvernadero, idzona=idzona)
    except ObjectDoesNotExist:
        return JsonResponse({}, safe=False)

    param = request.GET.get('param')
    startdate = request.GET.get('from')
    enddate = request.GET.get('to') 

    historiamodulo = Historiamodulo.objects.filter(idmodulo=idmodulo, fecharegistro__range=[startdate, enddate]).order_by('fecharegistro')

    if param == 'temp':
        historiamodulo = historiamodulo.values('temperatura', "fecharegistro")
    elif param == 'hum_tie':
        historiamodulo = historiamodulo.values('humedadtierra', "fecharegistro")
    elif param == 'hum_amb':
        historiamodulo = historiamodulo.values('humedadambiente', "fecharegistro")
    elif param == 'agua':
        historiamodulo = historiamodulo.values('nivelagua', "fecharegistro")
    elif param == 'co2':
        historiamodulo = historiamodulo.values('concentracionco2', "fecharegistro")
    else:
        historiamodulo = historiamodulo.values()

    return JsonResponse(list(historiamodulo), safe=False)