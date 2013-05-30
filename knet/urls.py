from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'knet.landing.views.landing', name='landing'),
    url(r'^demo/$', 'knet.views.demo', name='demo'),
    url(r'^teacher/(?P<teacher_id>\d+)/$',
        TemplateView.as_view(template_name='teacher_detail.html'),
        name='teacher_detail',
        ),
    url(r'^admin/', include(admin.site.urls)),
)
