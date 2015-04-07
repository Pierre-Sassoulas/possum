from django.conf.urls import patterns, url


urlpatterns = patterns('possum.jukebox.views',
                       url('^$', 'musicplayerd', name='jukebox_home'),
                       ('^playpl$', 'ajax_playpl'),
                       ('^playpause$', 'ajax_playpause'),
                       ('^next$', 'ajax_next'),
                       ('^previous$', 'ajax_previous'),
                       ('^info$', 'ajax_info'),
                       ('^remove$', 'ajax_remove'),
                       )
