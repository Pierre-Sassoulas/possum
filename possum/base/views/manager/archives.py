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

import datetime
import logging

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext as _

from possum.base.forms import DateForm
from possum.base.models import Facture
from possum.base.views import check_admin
from possum.stats.views import init_borders


LOG = logging.getLogger(__name__)


@user_passes_test(check_admin)
def archives(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context = init_borders(context)
    date = datetime.datetime.today()
    if request.method == 'POST':
        try:
            date = datetime.datetime.strptime(request.POST.get('date'),
                                              "%Y-%m-%d").date()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Date is not valid"))
#    context['date_form'] = DateForm({'date': date, })
    context['factures'] = Facture().get_bills_for(date)
    context['date'] = date
    return render(request, 'manager/archives/facture_list.html', context)


@user_passes_test(check_admin)
def archives_bill(request, bill_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param bill_id:
    :type bill_id:
    '''
    context = {'menu_manager': True, }
    bill = get_object_or_404(Facture, pk=bill_id)
    if not bill.est_soldee():
        messages.add_message(request, messages.ERROR,
                             _("This bill has not yet ended"))
        return redirect('archives')
    context['facture'] = bill
    context['products_sold'] = bill.reduced_sold_list(bill.produits.all())
    return render(request, 'manager/archives/facture_detail.html', context)
