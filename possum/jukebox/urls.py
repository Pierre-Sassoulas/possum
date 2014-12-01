from django.conf.urls import patterns, include, url


urlpatterns = patterns('possum.jukebox.views',
                       ('^$', 'musicplayerd'),
                       ('^play$', 'ajax_play'),
                       ('^pause$', 'ajax_pause'),
                       ('^next$', 'ajax_next'),
                       ('^previous$', 'ajax_previous'),
                       ('^info$', 'ajax_info'),
                       )
