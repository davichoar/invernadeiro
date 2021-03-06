from django.conf.urls import url, include
from app import views, api

urlpatterns = [

### LOGIN

    url('^$',
        views.login.index,
        name='loginIndex'),

### ESCOGER INVERNADERO

    url('^invernadero/$',
        views.invernadero.escoger,
        name='escogerInvernadero'),
        
### USUARIO
        
    url('^usuario/crear/$',
        views.usuario.crear,
        name='usuarioCrear'),        
    url('^usuario/$',
        views.usuario.listar,
        name='usuariosLista'),        
    url('^usuario/(?P<idUsuario>.*)$',
        views.usuario.detalle,
        name='usuarioDetalle'),

### PRUEBA JSON
        
    url('^pruebajson/$',
        views.pruebajson.prueba,
        name='pruebajson'),

### ZONA INVERNADERO

    url('^zonainvernadero/crear/$',
        views.zonaInvernadero.crear,
        name='zonaInvernaderoCrear'),
    url('^zonainvernadero/$',
        views.zonaInvernadero.listar,
        name='zonaInvernaderoListar'),
    url('^zonainvernadero/(?P<idZona>.*)$',
        views.zonaInvernadero.detalle,
        name='zonaInvernaderoDetalle'),

### INVERNADEROS
        
    url('^inv/crear/$',
        views.inv.crear,
        name='invernaderoCrear'),        
    url('^inv/$',
        views.inv.listar,
        name='invernaderoLista'),        
    url('^inv/(?P<idInv>.*)$',
        views.inv.detalle,
        name='invernaderoDetalle'),

### MODULO SEMILLA

    url('^modulosemilla/crear/$',
        views.moduloSemilla.crear,
        name='moduloSemillaCrear'),
    url('^modulosemilla/$',
        views.moduloSemilla.listar,
        name='moduloSemillaListar'),
    url('^modulosemilla/(?P<idModulo>.*)$',
        views.moduloSemilla.detalle,
        name='moduloSemillaDetalle'),
    url('^modulosemillafotos/(?P<idModulo>.*)$',
        views.moduloSemilla.fotos,
        name='moduloSemillaFotos'),
    url('^modulosemillacronograma/(?P<idModulo>.*)$',
        views.moduloSemilla.cronograma,
        name='moduloSemillaCronograma'),

### PLANTAS

    url('^planta/crear/$',
        views.planta.crear,
        name='plantaCrear'),
    url('^planta/$',
        views.planta.listar,
        name='plantaListar'),
    url('^planta/(?P<idPlanta>.*)$',
        views.planta.detalle,
        name='plantaDetalle'),

### PANEL LUZ

    url('^panel/crear/$',
        views.panelluz.crear,
        name='panelCrear'),
    url('^panel/$',
        views.panelluz.listar,
        name='panelListar'),
    url('^panel/(?P<idPanel>.*)$',
        views.panelluz.detalle,
        name='panelDetalle'),

### SEMILLAS

    url('^semilla/crear/(?P<idModulo>.*)/(?P<columna>.*)/(?P<fila>.*)$',
        views.semilla.crear,
        name='semillaCrear'),
    url('^semilla/(?P<idModulo>.*)/(?P<idSemilla>.*)$',
        views.semilla.detalle,
        name='semillaDetalle'),
        
### TIPO PLANTAS
        
    url('^tipoplanta/crear/$',
        views.tipoPlanta.crear,
        name='tipoPlantaCrear'),        
    url('^tipoplanta/$',
        views.tipoPlanta.listar,
        name='tipoPlantaListar'),        
    url('^tipoplanta/(?P<idTipoPlanta>.*)$',
        views.tipoPlanta.detalle,
        name='tipoPlantaDetalle'),

### HISTORIAS (RECIBIR JSONS)

    url('^historia/$',
            views.historia.prueba,
            name='historia'),

### AUDITORIA

    url('^auditoria/$',
        views.auditoria.veraudit,
        name='verAuditoria'),
    url('^auditoria/(?P<idAuditoria>.*)$',
        views.auditoria.detalleaudit,
        name='detalleAuditoria'),


### Cronograma

    url('^cronograma/$',
            views.cronograma.obtener,
            name='Cronograma'),

### GENTELELLA

    url(r'^.*\.html', views.views.gentella_html, name='gentella'),

### EL HOME

    url(r'^index/(?P<idInvernadero>.*)$', views.index, name='index'),

### CERRAR SESION
    
    url(r'^cerrarSesion/$', views.cerrarSesion, name='cerrarSesion'),

### CAMBIAR INVERNADERO
    
    url(r'^cambiarInvernadero/$', views.cambiarInvernadero, name='cambiarInvernadero'),

## ESTADISTICAS

    url(r'^estadisticas/$', views.estadisticas.stats_all, name='estadisticas'),
    url(r'^estadisticas/detalle/$', views.estadisticas.expanded_stats, name='estadisticas-detalle'),

## API PARA CONTENIDO DINAMICO
    url(r'^api/', include(api.apipatterns))
    
]