from django.conf.urls import patterns, include, url

from views import musicplayerd
from musicplayerd import ajax_play
from musicplayerd import ajax_pause
from musicplayerd import ajax_next
from musicplayerd import ajax_previous

from django.contrib import admin
from musicplayerd import ajax_info
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'possummpd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    ('^musicplayerd$', musicplayerd),
    ('^ajax/play$', ajax_play),
    ('^ajax/pause$', ajax_pause),
    ('^ajax/next$', ajax_next),
    ('^ajax/previous$', ajax_previous),
    ('^ajax/info$', ajax_info),
)
