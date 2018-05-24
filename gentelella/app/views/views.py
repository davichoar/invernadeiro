from django.template import loader
from django.http import HttpResponse

from app.models import Usuario


def index(request,nombreInvernadero):

    print('INDEX')
    print(nombreInvernadero)
    print('--------')
    print(request.session.get('idUsuarioActual'))
    request.session['nombreInvernadero'] = nombreInvernadero
    template = loader.get_template('app/index.html')
    idUsuario = request.session.get('idUsuarioActual')
    usuario = None
    try:
        usuario = Usuario.objects.get(idusuario=idUsuario)
    except:
        print('Error al consultar base de datos')
        return

    #nombreInvernadero = nombreInvernadero.replace(" ","")
    context = {
        'nombreUsuario': usuario.nombres,
        'nombreInvernadero': nombreInvernadero,
    }
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))



