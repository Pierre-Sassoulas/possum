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

import urllib2

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test

from possum.base.views import check_admin


@user_passes_test(check_admin)
def credits(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, 'version': settings.POSSUM_VERSION}
    return render(request, 'base/manager/credits.html', context)


@user_passes_test(check_admin)
def check_new_version(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    try:
        req = urllib2.Request('http://last.possum-software.org/', headers={
                              'User-Agent': 'Possum/' + settings.POSSUM_VERSION
                              })
        response = urllib2.urlopen(req)
        version = response.read().split('\n')[0]
    except:
        messages.add_message(request, messages.ERROR,
                             _("Impossible to get an answer"))
    else:
        if version != settings.POSSUM_VERSION:
            messages.add_message(request, messages.WARNING,
                                 "%s: %s" % (_("New release available"),
                                             version))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 _("You have last release"))

    return redirect('credits')
