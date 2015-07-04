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
from mpd import MPDClient
import json

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _

from .forms import PlaylistsForm


LOG = logging.getLogger(__name__)
playlist_names = list()


def check_cnx():
    """
    :return: Boolean about if the mpd server is reachable
    """
    if not settings.MPD_HOST:
        LOG.debug("settings.MPD_HOST not set !")
        return False
    try:
        # if previous errors, ignore them
        settings.MPD_CLIENT.clearerror()
        pingmpd = settings.MPD_CLIENT.ping()
        LOG.debug("settings.MPD_CLIENT " + pingmpd)
        return True
    except:
        try:
            LOG.debug("settings.MPD_CLIENT KO !")
            settings.MPD_CLIENT = MPDClient()
            # Timeout important to avoid freeze while using and testing
            settings.MPD_CLIENT.timeout = 2
            settings.MPD_CLIENT.connect(settings.MPD_HOST, settings.MPD_PORT)
            if settings.MPD_PWD:
                settings.MPD_CLIENT.password(settings.MPD_PWD)
            LOG.debug("settings.MPD_CLIENT OK (new instance) !")
            return True
        except:
            LOG.debug("settings.MPD_CLIENT KO (new instance) !")
            return False


def getinfos():
    """
    :return: Informations on the current playback
    """
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
            LOG.debug("error retriving state of mpd")
            return {'song': _("Error"), 'time': 0, }
    else:
        return {'song': _("Error"), 'time': 0, }


def make_playlist_names():
    """
    :return: A list of String corresponding to the playlist names
    """
    # reset the shared var playlist_names to build an updated list
    del playlist_names[:]
    playlist_names.append(('0', ''))
    if check_cnx():
        try:
            nowpl = settings.MPD_CLIENT.playlist()
            plists = settings.MPD_CLIENT.listplaylists()
            j = 1
            nowplfound = False
            for i in plists:
                if not nowplfound:
                    rqplfull = settings.MPD_CLIENT.listplaylistinfo(i['playlist'])
                    if not is_same_pl(nowpl, rqplfull):
                        playlist_names.append((j, i['playlist']))
                        j = j + 1
                    else:
                        playlist_names[0] = ('0', i['playlist'])
                        nowplfound = True
                else:
                    playlist_names.append((j, i['playlist']))
                    j = j + 1
        except:
            LOG.debug("error retrieving playlists names")


def musicplayerd(request):
    """
    :param HttpRequest request:
    :return rtype: HttpResponse
    """
    context = {'menu_jukebox': True, 'need_auto_refresh': 120}
    if check_cnx():
        if 'pl' in request.GET:
            change_pl(request.GET['pl'])
        pl_form = PlaylistsForm()
        make_playlist_names()
        pl_form.fields['pl'].choices = playlist_names
        context['pl_form'] = pl_form
        # append infos on current playback to the context
        context = dict(context.items() + getinfos().items())
        return render_to_response('jukebox/musicplayerd.html', context)
    else:
        context['jukebox_disable'] = True
        return render(request, 'jukebox/musicplayerd.html', context)


def is_same_pl(nowpl, rqplfull):
    """
    :param nowpl: the actual playlist from MPD_CLIENT.playlist
    :param rqplfull: the requested playlist from MPD_CLIENT.listplaylistinfo
    :return: Boolean
    """
    try:
        rqpl = list()
        # building a list like nowpl from rqplfull to compare
        for song in rqplfull:
            rqpl.append('file: ' + song['file'])
        return nowpl == rqpl
    except:
        LOG.debug("error comparing playlists: " + nowpl + " vs " + rqplfull)
        return True


def change_pl(plid):
    """
    :param Integer plid: the generated id of the playlist
    """
    if plid:
        if check_cnx():
            nowpl = settings.MPD_CLIENT.playlist()
            rqplname = playlist_names[int(plid)][1]
            rqplfull = settings.MPD_CLIENT.listplaylistinfo(rqplname)
            if not is_same_pl(nowpl, rqplfull):
                results = "error changing playlist : "
                try:
                    settings.MPD_CLIENT.clearerror()
                    # Prevents errors when multiple commands in a row
                    settings.MPD_CLIENT.command_list_ok_begin()
                    settings.MPD_CLIENT.stop()
                    settings.MPD_CLIENT.clear()
                    settings.MPD_CLIENT.load(rqplname)
                    settings.MPD_CLIENT.play()
                    # Tell server to execute commands and get feedback
                    results += settings.MPD_CLIENT.command_list_end()
                except:
                    LOG.debug(results)


def ajax_playpl(request):
    """
    :param HttpRequest request:
    :return rtype: HttpResponse
    """
    HTML_to_return = ''
    if check_cnx():
        try:
            if 'pl' in request.GET:
                change_pl(request.GET['pl'])
        except:
            LOG.debug("error while changing playlist")
    return HttpResponse(HTML_to_return)


def ajax_playpause(request):
    """
    :param HttpRequest request:
    """
    HTML_to_return = ''
    if check_cnx():
        try:
            status = settings.MPD_CLIENT.status()
            if (status['state'] == 'play'):
                settings.MPD_CLIENT.pause(1)
                return HttpResponse('paused')
            else:
                settings.MPD_CLIENT.play()
        except:
            LOG.debug("error while pressing play/pause")
    return HttpResponse(HTML_to_return)


def ajax_next(request):
    """
    :param HttpRequest request:
    """
    HTML_to_return = ''
    if check_cnx():
        try:
            settings.MPD_CLIENT.next()
        except:
            LOG.debug("error while pressing next")
    return HttpResponse(HTML_to_return)


def ajax_previous(request):
    """
    :param HttpRequest request:
    """
    HTML_to_return = ''
    if check_cnx():
        try:
            settings.MPD_CLIENT.previous()
        except:
            LOG.debug("error while pressing previous")
    return HttpResponse(HTML_to_return)


def ajax_info(request):
    """
    :param HttpRequest request:
    """
    HTML_to_return = ''
    try:
        infos = getinfos()
        HTML_to_return = json.dumps(infos)
    except:
        LOG.debug("error retriving song infos")
    return HttpResponse(HTML_to_return)


def ajax_remove(request):
    """
    :param HttpRequest request:
    """
    HTML_to_return = ''
    if check_cnx():
        try:
            status = settings.MPD_CLIENT.status()
            n = int(status['song'])
            settings.MPD_CLIENT.delete(n)
            if 'pl' in request.GET:
                plpos = int(request.GET['pl'])
                settings.MPD_CLIENT.playlistdelete(playlist_names[plpos][1], n)
            else:
                LOG.debug("error pressing remove : doesn't receive pl id")
        except:
            LOG.debug("error pressing remove")
    return HttpResponse(HTML_to_return)
