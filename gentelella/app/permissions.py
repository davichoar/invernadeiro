from app.models import Usuario, Rol, Permiso, Permisoxrol
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

def tienepermiso(request, permiso):
    permisosPedidos = Permiso.objects.filter(nombrepermiso = permiso, habilitado = True)
    permisosxrolUsuario = Permisoxrol.objects.filter(idrol = Usuario.objects.get(idusuario = request.session['idUsuarioActual']).idrol)
    for permisoxrol in permisosxrolUsuario:
        for permisoPedido in permisosPedidos:
            if permisoPedido.idpermiso == permisoxrol.idpermiso:
                return True
    return False
    
def accesodenegado(request):
    raise PermissionDenied
    #return render(request, 'app/page_403.html', {})