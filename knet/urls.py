from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'knet.landing.views.landing', name='landing'),
    url(r'^demo/$', 'knet.views.demo', name='demo'),
    url(r'^teacher/(?P<teacher_id>\d+)/$',
        'knet.stories.views.teacher_detail',
        name='teacher_detail',
        ),
    url(r'^admin/', include(admin.site.urls)),
)
