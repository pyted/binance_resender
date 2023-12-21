from django.contrib import admin
from django.urls import path, re_path, include
from django.views import static as view_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appSender.urls', namespace='appSender')),
    re_path(r'^static/(?P<path>.*)$', view_static.serve, {'document_root': 'static'}, name='static'),
]
