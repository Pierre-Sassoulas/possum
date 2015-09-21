from django.conf.urls import patterns, url


urlpatterns = patterns('possum.jukebox.views',
                       url('^$', 'home', name='home'),
                       url('^load/(?P<name>.*)/$', 'load', name='load'),
                       url('^next/$', 'next_song', name='next'),
                       url('^previous/$', 'previous_song', name='previous'),
                       url('^shuffle/$', 'shuffle', name='shuffle'),
                       url('^play/$', 'play', name='play'))
