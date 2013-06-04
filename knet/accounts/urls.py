from django.conf.urls import patterns, url

from .views import oauth


urlpatterns = patterns(
    '',
    url(r'^oauth/$', oauth, name='oauth'),
)
