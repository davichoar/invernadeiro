from django.conf.urls import url
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url('^$',
        views.login.index,
        name='loginIndex'),

    url(r'^.*\.html', views.views.gentella_html, name='gentella'),

    # The home page
    url(r'^index/$', views.index, name='index'),
]