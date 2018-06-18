from app.models import Historiaplanta, Planta, Zona
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def get(request):
    idplanta = request.GET.get('id')
    idzona = Planta.objects.get(idplanta=idplanta).idzona
    idinvernadero = request.session['idInvernadero']
    try:
        zona = Zona.objects.get(idinvernadero=idinvernadero, idzona=idzona)
    except ObjectDoesNotExist:
        return JsonResponse({}, safe=False)

    param = request.GET.get('param')
    startdate = request.GET.get('from')
    enddate = request.GET.get('to') 

    historiaplanta = Historiaplanta.objects.filter(idplanta=idplanta, fecharegistro__range=[startdate, enddate]).order_by('fecharegistro')

    if param == 'hum_amb':
        historiaplanta = historiaplanta.values('humedad', "fecharegistro")
    else:
        historiaplanta = historiaplanta.values()
    
    return JsonResponse(list(historiaplanta), safe=False)