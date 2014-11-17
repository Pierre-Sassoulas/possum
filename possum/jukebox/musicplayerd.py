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

from django.http import HttpResponse
from mpd import MPDClient, ConnectionError


client = MPDClient()


def check_cnx(aclient):
    '''
    :param aclient:
    :type aclient:
    '''
    try:
        aclient.status()
    except ConnectionError:
        try:
            aclient.connect("localhost", 8000)
        except:
            print "TODO: on doit tester les cas d'erreurs"
            return False


def ajax_play(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    HTML_to_return = ''
    check_cnx(client)
    if 'id' in request.GET:
        client.play(request.GET['id'])
    else:
        client.play()
    return HttpResponse(HTML_to_return)


def ajax_pause(request):
    '''
    :return rtype: HttpResponse
    '''
    HTML_to_return = ''
    check_cnx(client)
    client.pause(1)
    return HttpResponse(HTML_to_return)


def ajax_next(request):
    '''
    :return rtype: HttpResponse
    '''
    HTML_to_return = ''
    check_cnx(client)
    client.next()
    return HttpResponse(HTML_to_return)


def ajax_previous(request):
    '''
    :return rtype: HttpResponse
    '''
    HTML_to_return = ''
    check_cnx(client)
    client.previous()
    return HttpResponse(HTML_to_return)


def ajax_info(request):
    '''
    :return rtype: HttpResponse
    '''
    check_cnx(client)
    HTML_to_return = "Morceau : " + \
        client.status()['song'] + " , Temps : " + client.status()['elapsed']
    return HttpResponse(HTML_to_return)
