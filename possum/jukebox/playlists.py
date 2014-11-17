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

from django import forms
from mpd import MPDClient

from .musicplayerd import check_cnx


def make_playlist_names():
    '''
    :return: A list of String corresponding to the playlist names
    '''
    client = MPDClient()
    check_cnx(client)
    print "On doit tester le retour !!"
    return []
#    plists = client.listplaylists()
#    playlist_names = list()
#    for i in range(0, len(plists)):
#        playlist_names.append((plists[i]['playlist'], plists[i]['playlist']))
#    return playlist_names


class PlaylistsForm(forms.Form):

    '''
    The form for a Playlist.
    '''
    pl = forms.ChoiceField(label='Choose a playlist :',
                           choices=make_playlist_names())
