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
from django.utils.translation import ugettext as _
from mpd import MPDClient

from .musicplayerd import check_cnx


def make_playlist_names():
    '''
    :return: A list of String corresponding to the playlist names
    '''
    client = MPDClient()
    check_cnx(client)
    plists = client.listplaylists()
    playlist_names = list()
    playlist_names.append(('0', ''))
    for i in plists:
        playlist_names.append((i['playlist'], i['playlist']))
    playlist_names.append(('-1', _("Stop")))
    return playlist_names


class PlaylistsForm(forms.Form):

    '''
    The form for a Playlist.
    '''
    pl = forms.ChoiceField(label='',
                           choices=make_playlist_names())
