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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _


LOG = logging.getLogger(__name__)


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


def home(request):
    """
    :param HttpRequest request:
    """
    context = {'menu_jukebox': True, 'need_auto_refresh': 10}
    if check_cnx():
        listplaylists = settings.MPD_CLIENT.listplaylists()
        status = settings.MPD_CLIENT.status()
        # status['time'] = '80:130'
        #   80: time elapsed
        #   130: total time
        # state == play, stop, pause, ...
        context[status['state']] = True
        try:
            context["volume"] = status["volume"]
            elapsed, time = status['time'].split(":")
            context["pourcent"] = int(int(elapsed)*100 / int(time))
            infos = settings.MPD_CLIENT.currentsong()
            context["title"] = infos['title']
            context["artist"] = infos['artist']
        except:
            LOG.info("can't retrieve current song")
        context['playlists'] = [t['playlist'] for t in listplaylists]
    else:
        context['jukebox_disable'] = True
    return render(request, 'jukebox/home.html', context)


def load(request, name):
    """Load playlist 'name'
    :param request: HttpRequest
    :param name: name of a playlist (str)
    """
    if check_cnx():
        LOG.debug("try to load: %s" % name)
        try:
            settings.MPD_CLIENT.clearerror()
            # Prevents errors when multiple commands in a row
            settings.MPD_CLIENT.command_list_ok_begin()
            settings.MPD_CLIENT.stop()
            settings.MPD_CLIENT.clear()
            settings.MPD_CLIENT.load(name)
            settings.MPD_CLIENT.play()
            # Tell server to execute commands and get feedback
            settings.MPD_CLIENT.command_list_end()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Playlist can't be load"))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 _("Playlist loaded"))
    return redirect('jukebox:home')


def play(request):
    """play song
    :param request: HttpRequest
    """
    if check_cnx():
        try:
            status = settings.MPD_CLIENT.status()
            if (status['state'] == 'play'):
                LOG.debug("play >> pause")
                settings.MPD_CLIENT.pause(1)
            else:
                LOG.debug("play")
                settings.MPD_CLIENT.play()
        except:
            messages.add_message(request, messages.ERROR, _("Error"))
    return redirect("jukebox:home")


def next_song(request):
    """Next song
    :param request: HttpRequest
    """
    if check_cnx():
        try:
            LOG.debug("next song")
            settings.MPD_CLIENT.next()
        except:
            messages.add_message(request, messages.ERROR, _("Error"))
    return redirect("jukebox:home")


def shuffle(request):
    """Shuffle songs in playlist
    :param request: HttpRequest
    """
    if check_cnx():
        try:
            LOG.debug("shuffle")
            settings.MPD_CLIENT.shuffle()
        except:
            messages.add_message(request, messages.ERROR, _("Error"))
    return redirect("jukebox:home")


def previous_song(request):
    """Next song
    :param request: HttpRequest
    """
    if check_cnx():
        try:
            LOG.debug("previous song")
            settings.MPD_CLIENT.previous()
        except:
            messages.add_message(request, messages.ERROR, _("Error"))
    return redirect("jukebox:home")
