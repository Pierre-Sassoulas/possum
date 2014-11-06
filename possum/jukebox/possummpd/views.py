'''
@author: br0ne
'''
from django.shortcuts import render_to_response
from playlists import playlistsform
from mpd import MPDClient
from django.http import HttpResponse
from musicplayerd import check_cnx

client = MPDClient()

def musicplayerd(request): 
    if 'pl' in request.GET:
        check_cnx(client)
        client.stop()
        client.clear()
        client.load(request.GET['pl'])
        client.play()
    
    return render_to_response('musicplayerd.html', {'pl_form': playlistsform})