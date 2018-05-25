from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from app.models import Usuario



def index(request,
          template='app/loginShido.html',
          extra_context=None):

    #print(type(Usuario.objects.raw('Select * from app.usuario')))
    #print(type(Usuario.objects.all()))
    #print(request.method + ' q1 se la come')
    if request.method == 'POST':
        print('LLEGO POST')
        nombreUsuario = request.POST['nombreUsuario']
        contraseña = request.POST['contraseña']
        #usuario = Usuario.objects.raw('Select * from app.usuario where nombreusuario='+nombreUsuario+' and  contrasena = '+contraseña)
        #listaUsuario = Usuario.objects.raw('Select * from public.app.usuario')
        #listaUsuario = Usuario.objects.all()
        usuario = None
        try:
            usuario = Usuario.objects.get(nombreusuario=nombreUsuario, contrasena=contraseña)
        except:
            print('Error al consultar base de datos')

        if usuario is not None:
            print(usuario.nombres)
            print(usuario.apellidopaterno)
            request.session['idUsuarioActual'] = usuario.idusuario
            return redirect('escogerInvernadero')


    ##context = {
    #    'userList': user,
    #}
    context = {

     }
    if extra_context is not None:
        context.update(extra_context)
    if request.method == 'GET':
        if 'idUsuarioActual' in request.session:
            print(request.session['idUsuarioActual'])
            usuario = Usuario.objects.get(idusuario=request.session['idUsuarioActual'])
            if 'idInvernadero' in request.session:
                context = {
                    'nombreUsuario': usuario.getnombrecompleto(),
                    'idInvernadero': request.session['idInvernadero'],
                }
                template = loader.get_template('app/index.html')
                return HttpResponse(template.render(context, request))
            else:
                return redirect('escogerInvernadero')

    return render(request, template, context)