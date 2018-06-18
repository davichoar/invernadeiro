from app.models import Zona
from django.http import HttpResponse, JsonResponse

def get(request, idZone):
    idinvernadero = request.session['idInvernadero']
    zone = Zona.objects.all().filter(pk=idZone, idinvernadero=idinvernadero).values()
    return JsonResponse(list(zone), safe=False)