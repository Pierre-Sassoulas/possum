'''
@author: br0ne
'''
from mpd import MPDClient
from django.http import HttpResponse
from django.core.context_processors import request
from logilab.common.compat import json

client = MPDClient()

def check_cnx(aclient):
    try:
        aclient.status()
    except:
        aclient.connect("localhost", 6600)

def ajax_play(request):
    HTML_to_return = ''
    check_cnx(client)
    if 'id' in request.GET:
        client.play(request.GET['id'])
    else:
        client.play() 
    return HttpResponse(HTML_to_return)

def ajax_pause(request):
    HTML_to_return = ''
    check_cnx(client)
    client.pause(1)
    return HttpResponse(HTML_to_return)

def ajax_next(request):
    HTML_to_return = ''
    check_cnx(client)
    client.next()
    return HttpResponse(HTML_to_return)

def ajax_previous(request):
    HTML_to_return = ''
    check_cnx(client)
    client.previous()
    return HttpResponse(HTML_to_return)

def ajax_info(request):
    check_cnx(client)
    HTML_to_return = "Morceau : " + client.status()['song'] + " , Temps : " + client.status()['elapsed']
    return HttpResponse(HTML_to_return)