from django.template import loader
from django.http import HttpResponse

from app.models import Usuario, Invernadero


def cerrarSesion(request):
    request.session.pop('idUsuarioActual', None)
    request.session.pop('nombreInvernadero', None)
    request.session.pop('idInvernadero', None)
    template = loader.get_template('app/loginShido.html')
    context = {}
    return HttpResponse(template.render(context, request))


def index(request,idInvernadero):

    print('INDEX')
    print('IdInvernadero: '+idInvernadero)
    print('--------')
    print(request.session.get('idUsuarioActual'))
    request.session['idInvernadero'] = idInvernadero
    invernadero = Invernadero.objects.get(idinvernadero=idInvernadero)
    request.session['nombreInvernadero'] = invernadero.nombre
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
        'nombreUsuario': usuario.getnombrecompleto(),
        'nombreInvernadero':  invernadero.nombre,
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



