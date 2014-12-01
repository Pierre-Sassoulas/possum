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

from mpd import MPDClient, ConnectionError
from django.utils.translation import ugettext as _
from django.conf import settings


def check_cnx(aclient):
    ''' Check if the connection can be established, and establish it.

    :param MPDClient aclient:
    '''
    if not settings.MPD_HOST or not settings.MPD_PORT:
        return False
    try:
        aclient.status()
        return True
    except ConnectionError:
        try:
            aclient.connect(settings.MPD_HOST, settings.MPD_PORT)
            return True
        except:
            return False


def getinfos():
    client = MPDClient()
    if check_cnx(client):
        status = client.status()['state']
        if (status == 'play' or status == 'pause'):
            infos = {'song': client.currentsong()['title'],
                     'artist': client.currentsong()['artist'],
                     'elapsed': client.status()['elapsed'],
                     'time': client.currentsong()['time'],
                     }
            return infos
        else:
            return {'song': _("Stop"), 'time': 0, }
    else:
        return {'song': _("Error"), 'time': 0, }
