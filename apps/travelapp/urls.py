from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.travels),
    url(r'^users/register$', views.register),
    url(r'^users/login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add_travels),
    url(r'^travels/destination/(?P<travel_id>[0-9]+)$', views.destination),
    url(r'^travels/join/(?P<travel_id>[0-9]+)$', views.join),
]
