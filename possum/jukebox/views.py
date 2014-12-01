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
from django.http import HttpResponse
from mpd import MPDClient
import json

from .musicplayerd import check_cnx
from .musicplayerd import getinfos

from .forms import PlaylistsForm


def musicplayerd(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    client = MPDClient()
    if check_cnx(client):
        context = {'pl_form': PlaylistsForm,
                   'need_auto_refresh': 60,
                   }
        if 'pl' in request.GET:
            client.stop()
            client.clear()
            client.load(request.GET['pl'])
            client.play()
            context = dict(context.items() + getinfos().items())
        return render_to_response('jukebox/musicplayerd.html', context)
    else:
        return render_to_response('500.html')


def ajax_play(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    if 'pl' in request.GET:
        plname = request.GET['pl']
        if(plname != '0'):
            client.stop()
            client.clear()
            if(plname != '-1'):
                client.load(plname)
                client.play()
    else:
        client.play()
    return HttpResponse(HTML_to_return)


def ajax_pause(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    client.pause(1)
    return HttpResponse(HTML_to_return)


def ajax_next(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    client.next()
    return HttpResponse(HTML_to_return)


def ajax_previous(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    client.previous()
    return HttpResponse(HTML_to_return)


def ajax_info(request):
    client = MPDClient()
    check_cnx(client)
    infos = getinfos()
    HTML_to_return = json.dumps(infos)
    return HttpResponse(HTML_to_return)


def ajax_remove(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    client.delete()
    return HttpResponse(HTML_to_return)
