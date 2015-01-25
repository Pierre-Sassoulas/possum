from django.conf.urls import patterns, url


urlpatterns = patterns('possum.jukebox.views',
                       url('^$', 'musicplayerd', name='jukebox_home'),
                       ('^play$', 'ajax_play'),
                       ('^pause$', 'ajax_pause'),
                       ('^next$', 'ajax_next'),
                       ('^previous$', 'ajax_previous'),
                       ('^info$', 'ajax_info'),
                       )
