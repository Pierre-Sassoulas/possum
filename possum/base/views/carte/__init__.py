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
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test

from possum.base.forms import OptionForm
from possum.base.models import Categorie
from possum.base.models import Option
from possum.base.models import Produit
from possum.base.views import check_admin


LOGGER = logging.getLogger(__name__)


@user_passes_test(check_admin)
def carte(request):
    ''' This is not used.
    :param HttpRequest request:
    '''
    context = {'menu_manager': True, }
    return render(request, 'base/carte.html', context)


def is_valid_product(request, name, prize):
    '''
    TODO
    :param HttpRequest request:
    :param name:
    :type name:
    :param prize:
    :type prize:
    '''
    erreur = False
    if not name:
        erreur = True
        messages.add_message(request, messages.ERROR,
                             _("You must enter a name"))
    if not prize:
        erreur = True
        messages.add_message(request, messages.ERROR,
                             _("You must enter a price"))
    return not erreur


@user_passes_test(check_admin)
def products_view(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    context = {'menu_manager': True, }
    context['product'] = get_object_or_404(Produit, pk=product_id)
    if request.method == 'POST':
        context['option'] = OptionForm(request.POST)
        if context['option'].is_valid():
            context['option'].save()
    else:
        context['option'] = OptionForm()
    context['options'] = Option.objects.all()
    return render(request, 'base/carte/product.html', context)


@user_passes_test(check_admin)
def products_option(request, product_id, option_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param option_id:
    :type option_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    option = get_object_or_404(Option, pk=option_id)
    if option in product.options_ok.all():
        product.options_ok.remove(option)
    else:
        product.options_ok.add(option)
    product.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_new(request, category_id):
    '''
    TODO
    :param HttpRequest request:
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        prize = request.POST.get('prize', '').strip()
        if is_valid_product(request, name, prize):
            try:
                product = Produit(nom=name, prix=prize)
                product.set_category(context['category'])
                product.save()
            except Exception as ex:
                messages.add_message(request, messages.ERROR,
                                     _("Changes could not be saved"))
                LOGGER.warning(_("Changes could not be saved") + ": " + ex)
            else:
                return redirect('categories_view', context['category'].id)
    return render(request, 'base/carte/product_new.html', context)


@user_passes_test(check_admin)
def products_set_category(request, product_id, category_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param category_id:
    :type category_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    category = get_object_or_404(Categorie, pk=category_id)
    product.set_category(category)
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_category(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    context = {'menu_manager': True, }
    context['product'] = get_object_or_404(Produit, pk=product_id)
    context['categories'] = Categorie.objects.order_by('priorite', 'nom')
    return render(request, 'base/carte/product_category.html', context)


@user_passes_test(check_admin)
def products_del_produits_ok(request, product_id, sub_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param sub_id:
    :type sub_id:
    '''
    menu = get_object_or_404(Produit, pk=product_id)
    sub = get_object_or_404(Produit, pk=sub_id)
    menu.produits_ok.remove(sub)
    menu.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_select_produits_ok(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    context = {'menu_manager': True, }
    context['product'] = get_object_or_404(Produit, pk=product_id)
    context['products'] = []
    for category in context['product'].categories_ok.iterator():
        for sub in Produit.objects.filter(categorie=category, actif=True):
            if sub not in context['product'].produits_ok.iterator():
                context['products'].append(sub)
    return render(request, 'base/carte/product_select_produits_ok.html',
                  context)


@user_passes_test(check_admin)
def products_add_produits_ok(request, product_id, sub_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param sub_id:
    :type sub_id:
    '''
    menu = get_object_or_404(Produit, pk=product_id)
    product = get_object_or_404(Produit, pk=sub_id)
    menu.produits_ok.add(product)
    menu.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_del_categories_ok(request, product_id, category_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param category_id:
    :type category_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    category = get_object_or_404(Categorie, pk=category_id)
    product.categories_ok.remove(category)
    product.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_add_categories_ok(request, product_id, category_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    :param category_id:
    :type category_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    category = get_object_or_404(Categorie, pk=category_id)
    product.categories_ok.add(category)
    product.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_select_categories_ok(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    context = {'menu_manager': True, }
    context['product'] = get_object_or_404(Produit, pk=product_id)
    context['categories'] = []
    for category in Categorie.objects.order_by('priorite', 'nom').iterator():
        if category not in context['product'].categories_ok.iterator() \
                and category != context['product'].categorie:
            context['categories'].append(category)
    return render(request, 'base/carte/product_select_categories_ok.html',
                  context)


@user_passes_test(check_admin)
def products_cooking(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    new = not product.choix_cuisson
    product.choix_cuisson = new
    product.save()
    return redirect('products_view', product_id)


@user_passes_test(check_admin)
def products_enable(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    product = get_object_or_404(Produit, pk=product_id)
    new = not product.actif
    product.actif = new
    product.save()
    if product.actif:
        # si le produit est a nouveau actif, on mets a jour les informations
        # sur la TVA, ...
        new_product = product.update_vats()
        product = new_product
    return redirect('products_view', product.id)


@user_passes_test(check_admin)
def products_change(request, product_id):
    '''
    TODO
    :param HttpRequest request:
    :param product_id:
    :type product_id:
    '''
    context = {'menu_manager': True, }
    product = get_object_or_404(Produit, pk=product_id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        prize = request.POST.get('prize', '').strip().replace(',', '.')
        if is_valid_product(request, name, prize):
            new_product = product.set_prize(prize)
            new_product.nom = name
            try:
                new_product.save()
            except:
                messages.add_message(request, messages.ERROR,
                                     _("Changes could not be saved"))
            else:
                return redirect('products_view', new_product.id)
        else:
            LOGGER.debug("[P%s] invalid data" % product.id)
    context['product'] = product
    return render(request, 'base/carte/product_change.html', context)
