from django.urls import path, re_path
from appSender import views

app_name = 'appSender'
urlpatterns = [
    path('', views.index_handler, name='index'),
    re_path('^api/(?P<path>.+)$', views.api_handler, name='api'),
    re_path('^dapi/(?P<path>.+)$', views.dapi_handler, name='dapi'),
    re_path('^eapi/(?P<path>.+)$', views.eapi_handler, name='eapi'),
    re_path('^fapi/(?P<path>.+)$', views.fapi_handler, name='fapi'),
    re_path('^papi/(?P<path>.+)$', views.papi_handler, name='papi'),
]

