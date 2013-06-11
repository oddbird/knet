from django.conf.urls import patterns, url, include
from django.contrib import admin

from .landing.views import landing
from .teachers.views import teacher_detail, create_profile
from .views import demo
from .styleguide import styleguide

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', landing, name='landing'),
    url(r'^demo/$', demo, name='demo'),
    url(r'^teacher/(?P<username>.+)/$', teacher_detail, name='teacher_detail'),
    url(r'^profile/create/$', create_profile, name='create_profile'),
    url(r'^styleguide/$', styleguide, name='styleguide'),
    url(r'^accounts/', include('knet.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
