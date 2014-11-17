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

from django.shortcuts import render_to_response
from mpd import MPDClient

from .musicplayerd import check_cnx
from .playlists import PlaylistsForm


client = MPDClient()


def musicplayerd(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    if 'pl' in request.GET:
        check_cnx(client)
        client.stop()
        client.clear()
        client.load(request.GET['pl'])
        client.play()
    return render_to_response('jukebox/musicplayerd.html',
                              {'pl_form': PlaylistsForm})