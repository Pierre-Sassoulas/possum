'''
@author: br0ne
'''
from django import forms
from mpd import MPDClient
from musicplayerd import check_cnx

def makeplistnames():
    client = MPDClient()
    check_cnx(client)
    plists = client.listplaylists()

    PLAYLISTSNAMES = list()
    for i in range(0, len(plists)):
        PLAYLISTSNAMES.append((plists[i]['playlist'],plists[i]['playlist']))
    return PLAYLISTSNAMES

class playlistsform(forms.Form):
    '''
    classdocs
    '''
    pl = forms.ChoiceField(label='Choose a playlist :', choices=makeplistnames())
