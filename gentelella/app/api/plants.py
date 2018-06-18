from app.models import Planta
from django.http import HttpResponse, JsonResponse

def get(request):
    plants = Planta.objects.filter(habilitado = True)
    if (request.GET.get('idzona')):
        idzona = request.GET.get('idzona')
        plants = plants.filter(idzona=idzona)
    return JsonResponse(list(plants), safe=False)
