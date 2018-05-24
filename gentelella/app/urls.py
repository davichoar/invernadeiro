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

###
    url(r'^.*\.html', views.views.gentella_html, name='gentella'),

    # The home page
    url(r'^index/(?P<nombreInvernadero>.*)$', views.index, name='index'),
]