from django.conf.urls import url, include
from .zones import *
from .plants import *
from .stats import *

statspatterns = [
    url(r'^zone/$', stats.zone_stats)
]

apipatterns = [
    url(r'^stats/', include(statspatterns)),
    url(r'^zone/(?P<id_zone>.*)$', zones.get),
    url(r'^plants/$', plants.get)
]