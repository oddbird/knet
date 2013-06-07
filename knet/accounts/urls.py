from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^oauth/$', views.oauth, name='oauth'),
    url(r'^logout/$', views.logout, name='logout'),
)
