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

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test


from possum.base.models import Zone, Table
from possum.base.views import check_admin


LOG = logging.getLogger(__name__)


@user_passes_test(check_admin)
def tables_zone_delete(request, zone_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param zone_id:
    :type zone_id:
    '''
    context = {'menu_manager': True, }
    zone = get_object_or_404(Zone, pk=zone_id)
    if request.method == 'POST':
        # we are in post
        try:
            valid = request.POST['valid']
        except KeyError:
            LOG.warning("strange request from %s" % request.user)
        else:
            if valid == "ok":
                LOG.info("delete zone: %d" % zone.id)
                Table.objects.filter(zone=zone).delete()
                zone.delete()
                messages.add_message(request, messages.SUCCESS,
                                     _("Zone removed"))
            return redirect('tables')
    # first request
    context['zone'] = zone
    return render(request, 'base/manager/zone_remove.html', context)


@user_passes_test(check_admin)
def tables_table_new(request, zone_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param zone_id:
    :type zone_id:
    '''
    zone = get_object_or_404(Zone, pk=zone_id)
    table = Table(zone=zone)
    table.save()
    return redirect('tables_table', zone.id, table.id)


@user_passes_test(check_admin)
def tables_zone_new(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    zone = Zone()
    zone.save()
    return redirect('tables_zone', zone.id)


@user_passes_test(check_admin)
def tables_table(request, zone_id, table_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param zone_id:
    :type zone_id:
    :param table_id:
    :type table_id:
    '''
    context = {'menu_manager': True, }
    context['table'] = get_object_or_404(Table, pk=table_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        context['table'].nom = name
        try:
            context['table'].save()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Changes could not be saved"))
        else:
            return redirect('tables')
    return render(request, 'base/manager/table_detail.html', context)


@user_passes_test(check_admin)
def tables_zone(request, zone_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param zone_id:
    :type zone_id:
    '''
    context = {'menu_manager': True, }
    context['zone'] = get_object_or_404(Zone, pk=zone_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        context['zone'].nom = name
        try:
            context['zone'].save()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Changes could not be saved"))
        else:
            return redirect('tables')
    return render(request, 'base/manager/zone_detail.html', context)


@user_passes_test(check_admin)
def tables(request, zone_pk=0):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context['zones'] = Zone.objects.all()

    if zone_pk == 0:
        if len(context['zones']) > 0:
            context['zone'] = context['zones'][0]
            zone_pk = context['zone'].pk
    else:
        context['zone'] = get_object_or_404(Zone, pk=zone_pk)
    context['tables'] = Table.objects.filter(zone__pk=zone_pk)
    return render(request, 'base/manager/table_list.html', context)
