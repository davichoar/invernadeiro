from django.conf.urls import url
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.


##### PARA EL LOGIN

    url('^$',
        views.login.index,
        name='loginIndex'),

### PARA ESCOGER INVERNADERO

    url('^invernadero/$',
        views.invernadero.escoger,
        name='escogerInvernadero'),
        
    url('^usuario/$',
        views.usuario.crear,
        name='usuarioCrear'),
        
    url('^pruebajson/$',
        views.pruebajson.prueba,
        name='pruebajson'),

## ZONA INVERNADERO
    url('^zonainvernadero/crear/$',
        views.zonaInvernadero.crear,
        name='zonaInvernaderoCrear'),
    url('^zonainvernadero/$',
        views.zonaInvernadero.listar,
        name='zonaInvernaderoListar'),
    url('^zonainvernadero/(?P<idZona>.*)$',
        views.zonaInvernadero.detalle,
        name='zonaInvernaderoDetalle'),

    ###


###
    url(r'^.*\.html', views.views.gentella_html, name='gentella'),

    # The home page
    url(r'^index/(?P<idInvernadero>.*)$', views.index, name='index'),

    url(r'^cerrarSesion/$', views.cerrarSesion, name='cerrarSesion'),
]