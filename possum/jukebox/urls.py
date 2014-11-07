from django.conf.urls import patterns, include, url
from django.contrib import admin

from .musicplayerd import (ajax_info, ajax_next, ajax_pause, ajax_play,
                           ajax_previous)
from .views import musicplayerd


admin.autodiscover()

urlpatterns = patterns(url(r'^admin/', include(admin.site.urls)),
                       ('^musicplayerd$', musicplayerd),
                       ('^ajax/play$', ajax_play),
                       ('^ajax/pause$', ajax_pause),
                       ('^ajax/next$', ajax_next),
                       ('^ajax/previous$', ajax_previous),
                       ('^ajax/info$', ajax_info),
                       )
