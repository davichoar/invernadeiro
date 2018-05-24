from django.shortcuts import render, redirect

from app.models import Usuario, Invernadero, Usuarioxinvernadero


def escoger(request,
          template='app/escogerInvernadero.html',
          extra_context=None):

    print('ESCOGER INVERANDERO')

    idUsuario = request.session.get('idUsuarioActual')
    usuario = None
    try:
        usuario = Usuario.objects.get(idusuario=idUsuario)
    except:
        print('Error al consultar base de datos')
        return

    if usuario is not None:

        listaInvernaderoXUsuario = Usuarioxinvernadero.objects.filter(idusuario=idUsuario)
        listaInvernaderos = []

        if len(listaInvernaderoXUsuario) == 0:
            print('NINGUN INVERNADERO ASOCIADO A ESE USUARIO')
            return

        for item in listaInvernaderoXUsuario:
            print(item.idinvernadero)
            invernadero = Invernadero.objects.get(idinvernadero=item.idinvernadero)
            print(invernadero.nombre)
            listaInvernaderos.append(invernadero)
        context = {
            'listaInvernaderos': listaInvernaderos,
            'nombreUsuario': usuario.nombres,
        }

        print(usuario.nombres)
        ## si solo hay un invernadero
        if len(listaInvernaderos) == 1:
            return redirect('index',nombreInvernadero= listaInvernaderos[0].nombre)


        if extra_context is not None:
            context.update(extra_context)
        return render(request, template, context)
    else:
        return