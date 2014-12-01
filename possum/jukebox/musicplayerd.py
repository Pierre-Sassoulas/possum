'''
@author: br0ne
'''
from mpd import MPDClient
from django.utils.translation import ugettext as _


def check_cnx(aclient):
    try:
        aclient.status()
        return True
    except:
        try:
            aclient.connect("localhost", 8000)
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
