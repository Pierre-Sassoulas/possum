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
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from possum.base.models import Config, Facture


LOGGER = logging.getLogger(__name__)


def check_admin(user):
    """User is an admin ?
    """
    return user.is_superuser


@login_required
def cleanup_payment(request):
    """Remove all variables used for a new payment
    """
    keys = ['is_left', 'left', 'right', 'type_selected', 'tickets_count',
            'ticket_value', 'init_montant']
    for key in keys:
        if key in request.session.keys():
            del request.session[key]


@login_required
def remove_edition(request):
    """Remove 'bill_in_use' and update bill if found.
       This is use to reserve access to a bill.
    """
    if "bill_in_use" in request.session.keys():
        bill_id = request.session['bill_in_use']
        try:
            bill = Facture.objects.get(pk=bill_id)
        except Facture.DoesNotExist:
            LOGGER("[%s] bill is not here!" % bill_id)
        else:
            if "products_modified" in request.session.keys():
                # we update bill only once
                bill.update()
                bill.update_kitchen()
                request.session.pop("products_modified")
            bill.in_use_by = None
            bill.save()
            LOGGER.debug("[F%s] edition mode removed" % bill_id)
        request.session.pop("bill_in_use")
    cleanup_payment(request)
    return request


@login_required
def home(request):
    return redirect('bill_home')
    # request = remove_edition(request)
    # context = {'menu_home': True, }
    # return render(request, 'home.html', context)


@login_required
def shutdown(request):
    context = {'menu_manager': True, }
    config = Config.objects.filter(key="default_shutdown")
    if config:
        cmd = config[0].value
    else:
        cmd = "sudo /sbin/shutdown -h now"

    if os.path.isfile(settings.LOCK_STATS):
        messages.add_message(request, messages.ERROR,
                             _("Statistics being calculated, please wait"))
    else:
        if request.method == 'POST':
            os.system(cmd)
            messages.add_message(request, messages.SUCCESS,
                                 _("Server shutting down"))
            return redirect('home')
    return render(request, 'shutdown.html', context)
