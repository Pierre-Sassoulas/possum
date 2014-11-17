from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('possum.jukebox.views',
                       ('^musicplayerd/$', 'musicplayerd'),)

urlpatterns += patterns('possum.jukebox.musicplayerd',
                        ('^ajax/play$', 'ajax_play'),
                        ('^ajax/pause$', 'ajax_pause'),
                        ('^ajax/next$', 'ajax_next'),
                        ('^ajax/previous$', 'ajax_previous'),
                        ('^ajax/info$', 'ajax_info'),
                        )
