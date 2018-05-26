from django.http import HttpResponse

def prueba(request, template=None, extra_context=None):
    if request.method == 'GET':
        content = 'prueba del servidor'
        print('prueba del servidor')
        return HttpResponse(content, content_type='text/plain')
    if request.method == 'POST':
        cadena = request.body
        print(cadena)
        return HTTPResponse('ok', content_type='text/plain')