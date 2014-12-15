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
import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext as _
from mpd import MPDClient
import json

from .forms import PlaylistsForm

LOGGER = logging.getLogger(__name__)

def check_cnx():
    if not settings.MPD_HOST:
        LOGGER.debug("settings.MPD_HOST not set !")
        return False
    try:
        settings.MPD_CLIENT.ping()
        LOGGER.debug("settings.MPD_CLIENT OK !")
        return True
    except:
        try:
            LOGGER.debug("settings.MPD_CLIENT KO !")
            settings.MPD_CLIENT = MPDClient()
            settings.MPD_CLIENT.timeout = 2
            if settings.MPD_PWD:
                settings.MPD_CLIENT.password(settings.MPD_PWD)
            settings.MPD_CLIENT.connect(settings.MPD_HOST, settings.MPD_PORT)
            LOGGER.debug("settings.MPD_CLIENT OK (new instance) !")
            return True
        except:
            LOGGER.debug("settings.MPD_CLIENT KO (new instance) !")
            return False


def getinfos():
    if check_cnx():
        status = settings.MPD_CLIENT.status()
        try:
            if (status['state'] == 'play' or status['state'] == 'pause'):
                currsong = settings.MPD_CLIENT.currentsong()
                infos = {'song': currsong['title'],
                         'artist': currsong['artist'],
                         'elapsed': status['elapsed'],
                         'time': currsong['time'],
                         'status': status['state'], }
                return infos
            else:
                return {'song': _("Stop"), 'time': 0, }
        except:
            LOGGER.debug("error retriving state of mpd")
            return {'song': _("Error"), 'time': 0, }
    else:
        return {'song': _("Error"), 'time': 0, }


def make_playlist_names():
    '''
    :return: A list of String corresponding to the playlist names
    '''
    playlist_names = list()
    playlist_names.append(('0', ''))
    if check_cnx():
        plists = settings.MPD_CLIENT.listplaylists()
        for i in plists:
            playlist_names.append((i['playlist'], i['playlist']))
    playlist_names.append(('-1', _("Stop")))
    return playlist_names


def musicplayerd(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    if check_cnx():
        plnames = make_playlist_names()
        pl_form = PlaylistsForm()
        pl_form.fields['pl'].choices = plnames
        context = {'pl_form': pl_form,
                   'need_auto_refresh': 120, }
        if 'pl' in request.GET:
            if request.GET['pl'] != '0':
                if request.GET['pl'] != '-1':
                    nowpl = settings.MPD_CLIENT.playlist()
                    rqplfull = settings.MPD_CLIENT.listplaylistinfo(
                        request.GET['pl'])
                    if not is_same_pl(nowpl,rqplfull):
                        settings.MPD_CLIENT.stop()
                        settings.MPD_CLIENT.clear()
                        settings.MPD_CLIENT.load(request.GET['pl'])
                        settings.MPD_CLIENT.play()
                else:
                    settings.MPD_CLIENT.stop()
                    settings.MPD_CLIENT.clear()
        context = dict(context.items() + getinfos().items())
        return render_to_response('jukebox/musicplayerd.html', context)
    else:
        return render_to_response('500.html')

def is_same_pl(nowpl,rqplfull):
    '''
    :param nowpl: the actual playlist from MPD_CLIENT.playlist
    :param rqplfull: the requested playlist from MPD_CLIENT.listplaylistinfo
    :return: Boolean
    '''
    rqpl = list()
    for song in rqplfull:
        rqpl.append('file: ' + song['file'])
    return nowpl == rqpl

def ajax_play(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    HTML_to_return = ''
    if check_cnx():
        if 'pl' in request.GET:
            plname = request.GET['pl']
            if(plname != '0'):
                settings.MPD_CLIENT.stop()
                settings.MPD_CLIENT.clear()
                if(plname != '-1'):
                    settings.MPD_CLIENT.load(plname)
                    settings.MPD_CLIENT.play()
        else:
            settings.MPD_CLIENT.play()
    return HttpResponse(HTML_to_return)


def ajax_pause(request):
    '''
    :param HttpRequest request:
    '''
    HTML_to_return = ''
    if check_cnx():
        settings.MPD_CLIENT.pause(1)
    return HttpResponse(HTML_to_return)


def ajax_next(request):
    '''
    :param HttpRequest request:
    '''
    HTML_to_return = ''
    if check_cnx():
        settings.MPD_CLIENT.next()
    return HttpResponse(HTML_to_return)


def ajax_previous(request):
    '''
    :param HttpRequest request:
    '''
    HTML_to_return = ''
    if check_cnx():
        settings.MPD_CLIENT.previous()
    return HttpResponse(HTML_to_return)


def ajax_info(request):
    '''
    :param HttpRequest request:
    '''
    infos = getinfos()
    HTML_to_return = json.dumps(infos)
    return HttpResponse(HTML_to_return)


def ajax_remove(request):
    '''
    :param HttpRequest request:
    '''
    HTML_to_return = ''
    if check_cnx():
        settings.MPD_CLIENT.delete()
    return HttpResponse(HTML_to_return)
