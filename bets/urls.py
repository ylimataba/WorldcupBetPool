from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^veikkaa/1/$', views.lohkovaihe, name='lohkovaihe'),
    #url(r'^veikkaa/2/$', views.maalikuningas, name='maalikuningas'),
    #url(r'^veikkaa/3/$', views.kolmikko, name='kolmikko'),
    url(r'^veikkaa/4/$', views.pudotuspelit, name='pudotuspelit'),
    url(r'^tilanne$', views.tilanne, name='tilanne'),
    url(r'^vertaile$', views.vertaile, name='vertaile'),
]

