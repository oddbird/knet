from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from .landing.views import landing
from .teachers.views import teacher_detail
from .views import demo

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', landing, name='landing'),
    url(r'^demo/$', demo, name='demo'),
    url(r'^teacher/(?P<username>.+)/$', teacher_detail, name='teacher_detail'),
    url(r'^styleguide/$',
        TemplateView.as_view(template_name='styleguide/styleguide.html'),
        name='styleguide',
        ),
    url(r'^accounts/', include('knet.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
