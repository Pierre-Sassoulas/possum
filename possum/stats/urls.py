# -*- coding: utf-8 -*-
#
#    Copyright 2009-2014 Sébastien Bonnegent
#
#    This file is part of POSSUM.
#
#    POSSUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    POSSUM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with POSSUM.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls import patterns, url


urlpatterns = patterns('possum.stats.views',
                       url(r'^update/$', 'update', name='stats_update'),
                       url(r'^text/$', 'text', name='stats_text'),
                       url(r'^charts/$', 'charts', name='stats_charts'),
                       url(r'^dump/(?P<rapport>\d+)/(?P<interval>[a,y,m,w,d])/(?P<date_begin>\d{4}-\d{1,2}-\d{1,2})/(?P<date_end>\d{4}-\d{1,2}-\d{1,2})/$', 'dump', name='stats_dump'),
                       )
