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


LOGGER = logging.getLogger(__name__)


@user_passes_test(check_admin)
def archives(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    if request.method == 'POST':
        try:
            year = int(request.POST.get('date_year'))
            month = int(request.POST.get('date_month'))
            day = int(request.POST.get('date_day'))
            date = datetime.datetime(year, month, day)
        except:
            messages.add_message(request, messages.ERROR,
                                 _("The date is not valid"))
            date = datetime.datetime.today()
    else:
        date = datetime.datetime.today()
    context['date_form'] = DateForm({'date': date, })
    context['factures'] = Facture().get_bills_for(date)
    context['date'] = date
    return render(request, 'base/manager/archives/home.html', context)


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
    context['bill'] = bill
    context['products_sold'] = bill.reduced_sold_list(bill.produits.all())
    return render(request, 'base/manager/archives/invoice.html', context)
