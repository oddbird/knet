from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'knet.views.home', name='home'),
    url(r'^demo/$', 'knet.views.demo', name='demo'),
    url(r'^admin/', include(admin.site.urls)),
)
