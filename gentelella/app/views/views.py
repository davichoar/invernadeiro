from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

from app.models import Usuario, Invernadero


def cerrarSesion(request):
    request.session.pop('idUsuarioActual', None)
    request.session.pop('nombreInvernadero', None)
    request.session.pop('idInvernadero', None)
    request.session.pop('nomreUsuario', None)
    return redirect('loginIndex')

def cambiarInvernadero(request):
    request.session.pop('nombreInvernadero', None)
    request.session.pop('idInvernadero', None)
    return redirect('escogerInvernadero')


def index(request,idInvernadero):

    print('INDEX')
    print('IdInvernadero: '+idInvernadero)
    print('--------')
    idUsuario = int (request.session.get('idUsuarioActual'))
    print('IdUsuario Logueado:'+ (str (idUsuario)))
    request.session['idInvernadero'] = idInvernadero
    invernadero = Invernadero.objects.get(idinvernadero=idInvernadero)
    request.session['nombreInvernadero'] = invernadero.nombre
    template = loader.get_template('app/index.html')
    usuario = None
    try:
        usuario = Usuario.objects.get(idusuario=idUsuario)
    except:
        print('Error al consultar base de datos')
        return

    nombreUsuarioCompleto = usuario.getnombrecompleto()
    request.session['nomreUsuario'] = nombreUsuarioCompleto
    #nombreInvernadero = nombreInvernadero.replace(" ","")
    context = {
        'nombreUsuario': nombreUsuarioCompleto,
        'nombreInvernadero':  invernadero.nombre,
    }
    #return HttpResponse(template.render(context, request))
    return redirect('zonaInvernaderoListar')


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))



