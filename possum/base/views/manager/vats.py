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

from possum.base.models import Produit
from possum.base.models import VAT
from possum.base.views import check_admin


LOG = logging.getLogger(__name__)


@user_passes_test(check_admin)
def vats(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context['vats'] = VAT.objects.order_by('name')
    return render(request, 'manager/vats/vat_list.html', context)


def check_name_and_tax(request, name, tax):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param name:
    :type name:
    :param tax:
    :type tax:
    '''
    if not name:
        messages.add_message(request, messages.ERROR,
                             _("You must enter a name"))
    if not tax:
        messages.add_message(request, messages.ERROR,
                             _("You must enter a percentage tax"))


@user_passes_test(check_admin)
def vats_change(request, vat_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param vat_id:
    :type vat_id:
    '''
    context = {'menu_manager': True, }
    context['vat'] = get_object_or_404(VAT, pk=vat_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        tax = request.POST.get('tax', '').strip().replace(',', '.')
        check_name_and_tax(request, name, tax)
        p_filter = Produit.objects.filter
        try:
            context['vat'].name = name
            context['vat'].save()
            context['vat'].set_tax(tax)
            for product in p_filter(categorie__vat_onsite=context['vat']):
                product.update_vats()
            for product in p_filter(categorie__vat_takeaway=context['vat']):
                product.update_vats()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Changes could not be saved"))
        else:
            return redirect('vats')
    return render(request, 'manager/vats/vat_detail.html', context)


@user_passes_test(check_admin)
def vat_new(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context['vats'] = VAT.objects.order_by('name')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        tax = request.POST.get('tax', '').strip().replace(",", ".")
        check_name_and_tax(request, name, tax)
        try:
            vat = VAT(name=name)
            vat.set_tax(tax)
            vat.save()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Changes could not be saved"))
        else:
            return redirect('vats')
    return render(request, 'manager/vats/new.html', context)
