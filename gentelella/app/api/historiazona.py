from app.models import Zona, Historiazona
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def get(request):
    idzona = request.GET.get('id')
    idinvernadero = request.session['idInvernadero']
    try:
        zona = Zona.objects.get(idinvernadero=idinvernadero, idzona=idzona)
    except ObjectDoesNotExist:
        return JsonResponse({}, safe=False)

    param = request.GET.get('param')
    startdate = request.GET.get('from')
    enddate = request.GET.get('to') 

    historiazona = Historiazona.objects.filter(idzona=idzona, fecharegistro__range=[startdate, enddate]).order_by('fecharegistro')

    if param == 'temp':
        historiazona = historiazona.values('temperatura', "fecharegistro")
    elif param == 'ph':
        historiazona = historiazona.values('ph', "fecharegistro")
    elif param == 'co2':
        historiazona = historiazona.values('concentracionco2', "fecharegistro")
    else:
        historiazona = historiazona.values()
    
    return JsonResponse(list(historiazona), safe=False)


