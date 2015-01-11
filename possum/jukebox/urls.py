from django.conf.urls import patterns, include, url


urlpatterns = patterns('possum.jukebox.views',
                       ('^$', 'musicplayerd'),
                       ('^playpl$', 'ajax_playpl'),
                       ('^playpause$', 'ajax_playpause'),
                       ('^next$', 'ajax_next'),
                       ('^previous$', 'ajax_previous'),
                       ('^info$', 'ajax_info'),
                       ('^remove$', 'ajax_remove'),
                       )
