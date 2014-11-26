from django.conf.urls import patterns, include, url


urlpatterns = patterns('possum.jukebox.views',
                       ('^$', 'musicplayerd'),
                       ('^ajax/play$', 'ajax_play'),
                       ('^ajax/pause$', 'ajax_pause'),
                       ('^ajax/next$', 'ajax_next'),
                       ('^ajax/previous$', 'ajax_previous'),
                       ('^ajax/info$', 'ajax_info'),
                       )
