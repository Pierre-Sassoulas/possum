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
from django.utils.translation import ugettext as _
from mpd import MPDClient
import json

from .forms import PlaylistsForm

def check_cnx(aclient):
    try:
        aclient.status()
        return True
    except:
        try:
            aclient.timeout = 2
            aclient.connect("localhost", 6600)
            return True
        except:
            return False

def getinfos():
    client = MPDClient()
    if check_cnx(client):
        status = client.status()['state']
        if (status == 'play' or status == 'pause'):
            infos = {'song':client.currentsong()['title'],
                     'artist':client.currentsong()['artist'],
                     'elapsed':client.status()['elapsed'],
                     'time':client.currentsong()['time'],
                     }
            return infos
        else:
            return {'song': _("Stop"), 'time':0,}
    else:
        return {'song': _("Error"), 'time':0,}

def make_playlist_names(client):
    '''
    :return: A list of String corresponding to the playlist names
    '''
    playlist_names = list()
    playlist_names.append(('0', ''))
    if check_cnx(client) :
        plists = client.listplaylists()
        for i in plists:
            playlist_names.append((i['playlist'], i['playlist']))
    playlist_names.append(('-1', _("Stop")))
    return playlist_names

def musicplayerd(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    client = MPDClient()
    if check_cnx(client) :
        plnames = make_playlist_names(client)
        pl_form = PlaylistsForm()
        pl_form.fields['pl'].choices = plnames
        context = {'pl_form': pl_form,
    	           'need_auto_refresh': 60,
    	           }
        if 'pl' in request.GET:
            if request.GET['pl'] != '0' :
                if request.GET['pl'] != '-1':
                    nowpl = client.playlist()
                    rqplfull = client.listplaylistinfo(request.GET['pl'])
                    rqpl = list()
                    for song in rqplfull :
                        rqpl.append('file: '+song['file'])
                    if not nowpl == rqpl :
                        client.stop()
                        client.clear()
                        client.load(request.GET['pl'])
                        client.play()
                else :
                    client.stop()
                    client.clear()
        context = dict(context.items() + getinfos().items())
        return render_to_response('jukebox/musicplayerd.html',context)
    else:
        return render_to_response('500.html')

def ajax_play(request):
    HTML_to_return = ''
    client = MPDClient()
    check_cnx(client)
    if 'pl' in request.GET:
    	plname = request.GET['pl']
        if(plname!='0'):
            client.stop()
            client.clear()
            if(plname!='-1'):
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
