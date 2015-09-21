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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from possum.base.models import Facture
from possum.base.models import Follow


LOGGER = logging.getLogger(__name__)


@login_required
def kitchen(request):
    ''' Affiche la liste plats qui ne sont pas encore
    préparés
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_kitchen': True, }
    liste = []
    for bill in Facture().non_soldees():
        if bill.following.count():
            bill.follow = bill.following.latest()
            if not bill.follow.done:
                # on enlève les ProduitVendu de type menu
                todo = bill.follow.produits.\
                    filter(produit__categories_ok__isnull=True)
                bill.todo = bill.reduced_sold_list(todo, full=True)
                if bill.category_to_follow:
                    category_to_follow = bill.category_to_follow
                    after = bill.get_products_for_category(category_to_follow)
                    bill.after = bill.reduced_sold_list(after, full=True)
                liste.append(bill)
    context['factures'] = liste
    context['need_auto_refresh'] = 60
    return render(request, 'kitchen/home.html', context)


@login_required
def follow_done(request, follow_id):
    ''' All is ready for this table ?
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    follow = get_object_or_404(Follow, pk=follow_id)
    follow.done = True
    follow.save()
    return redirect('kitchen')


@login_required
def kitchen_for_bill(request, bill_id):
    '''
    :param request:
    :type request:
    :param bill_id:
    :type bill_id:
    '''
    context = {'menu_kitchen': True, }
    context['facture'] = get_object_or_404(Facture, pk=bill_id)
    if context['facture'].est_soldee():
        messages.add_message(request, messages.ERROR,
                             _("This invoice has already been ended"))
        return redirect('kitchen')
    return render(request, 'kitchen/view.html', context)
