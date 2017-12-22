from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^display$', views.display, name="display"),
    url(r'^add$', views.add, name="add"),
    url(r'^create$', views.create, name="create"),
    url(r'^info/(?P<product_id>\d+)$', views.info, name="info"),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<product_id>\d+)$', views.delete),
    url(r'^join/(?P<product_id>\d+)$', views.join),
    url(r'^leave/(?P<product_id>\d+)$', views.leave, name='leave'),    
]