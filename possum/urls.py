from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('possum.base.views',
    (r'^$', 'accueil'),
    (r'^accueil$', 'accueil'),
    (r'^carte$', 'carte'),
    (r'^pos$', 'pos'),
    (r'^bills$', 'factures'),
    (r'^jukebox$', 'jukebox'),
    (r'^stats$', 'stats'),
    (r'^users$', 'users'),
    (r'^accounts/login/$', 'my_login'),
    (r'^accounts/logout/$', 'my_logout'),
    (r'^facture/(?P<id_facture>\d+)/$', 'facture'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/pos/possum/static/'}),
    )
