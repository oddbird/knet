from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'knet.views.home', name='home'),
    url(r'^demo/$', 'knet.views.demo', name='demo'),
)
