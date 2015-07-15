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

from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from possum.base.forms import NoteForm
from possum.base.models import (Categorie, Config, Facture, Note, Option,
                                PaiementType, Paiement, Printer, Produit,
                                ProduitVendu, Zone, Table)
from possum.base.views import remove_edition, cleanup_payment


LOG = logging.getLogger(__name__)


@login_required
def bill_new(request):
    """ Create a new bill.
    :param HttpRequest request:
    """
    context = {'menu_bills': True, }
    bill = Facture()
    bill.save()
    return redirect("bill_view", bill.id)


def set_option(sold_id, option_id):
    """
    Enable/Disable an Option on a ProduitVendu.
    :param sold_id: TODO
    :type sold_id:
    :param option_id:
    :type option_id:
    """
    """
    """
    sold = get_object_or_404(ProduitVendu, pk=sold_id)
    option = get_object_or_404(Option, pk=option_id)
    if option in sold.options.all():
        sold.options.remove(option)
    else:
        sold.options.add(option)
    sold.save()


@login_required
def bill_send_kitchen(request, bill_id):
    """ Send in the kitchen
    :param HttpRequest request: TODO
    :param bill_id:
    :type bill_id:
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    erreur = False
    if not bill.table:
        erreur = True
        messages.add_message(request, messages.ERROR,
                             _("You must choose a table"))
    if not bill.couverts:
        erreur = True
        messages.add_message(request, messages.ERROR,
                             _("You must specify the number of guests"))
    if not erreur and not bill.print_ticket_kitchen():
        erreur = True
        messages.add_message(request, messages.ERROR,
                             _("Error in printing (printer ok?)"))
    if not erreur:
        LOG.info("[F%s] sent" % bill.id)
    return redirect('bill_view', bill.id)


@login_required
def bill_print(request, bill_id):
    """
    Print the bill.
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    if bill.is_empty():
        messages.add_message(request, messages.ERROR, _("No product"))
    else:
        printers = Printer.objects.filter(billing=True)
        if printers.count() == 0:
            messages.add_message(request, messages.ERROR,
                                 _("No printer configured"))
        else:
            if bill.print_ticket():
                messages.add_message(request, messages.SUCCESS,
                                     _("The bill is printed"))
            else:
                messages.add_message(request, messages.ERROR,
                                     _("Printing has failed"))
    return redirect('bill_view', bill.id)


@login_required
def table_select(request, bill_id, zone_pk=0):
    """ Select/modify table of a bill
    :param HttpRequest request:
    :param bill_id: TODO
    :type bill_id:
    """
    context = {'menu_bills': True, }
    context['zones'] = Zone.objects.all()
    context['bill_id'] = bill_id

    if zone_pk == 0:
        if len(context['zones']) > 0 :
            context['zone'] = context['zones'][0]
            zone_pk = context['zone'].pk
    else:
        context['zone'] = get_object_or_404(Zone, pk=zone_pk)
    context['tables'] = Table.objects.filter(zone__pk=zone_pk)
    return render(request, 'bill/select_a_table.html', context)


@login_required
def table_set(request, bill_id, table_id):
    """ Select/modify table of a bill

    :param HttpRequest request:
    :param bill_id: TODO
    :type bill_id:
    :param table_id:
    :type table_id:
    """
    context = {'menu_bills': True, }
    bill = get_object_or_404(Facture, pk=bill_id)
    table = get_object_or_404(Table, pk=table_id)
    bill.set_table(table)
    bill.save()
    return redirect("bill_view", bill.id)


@login_required
def set_number(request, bill_id, count):
    """ Set number of products to add

    :param HttpRequest request:
    :param bill_id: TODO
    :type bill_id:
    :param count:
    :type count:
    """
    request.session['count'] = int(count)
    return redirect('bill_categories', bill_id)


def update_session_number_of_product(request, bill_id, count):
    """ This function update the value for the number of product we want to
    add in bill/categories.

    :param HttpRequest request:
    :param int bill_id: Useless parameter in order to use the same URL as the
    mother page.
    :param count: The value we want to update.
    """
    request.session['count'] = int(count)
    return HttpResponse('OK')


@login_required
def categories(request, bill_id, category_id=None):
    """ Select a product to add on a bill.

    :param HttpRequest request:
    :param int bill_id: The id of the bill
    :param int category_id: The id of the category
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    if not set_edition_status(request, bill):
        return redirect('bill_view', bill.id)
    lcc = request.session.get('last_carte_changed')
    if lcc is None or Config().carte_changed(lcc):
        # If they are no categorie or if the carte changed
        lcc = Config().get_carte_changed().value
        request.session['last_carte_changed'] = lcc
        categories = []
        for category in Categorie.objects.all():
            products = Produit.objects.filter(categorie=category, actif=True)
            if products:
                category.products = products
                categories.append(category)
            else:
                LOG.debug("[%s] category without products" % category)
        LOG.debug("Updating session categories : '{0}'".format(categories))
        request.session['categories'] = categories
    else:
        # request.session['categories'] is not None
        LOG.debug('Use categories in cache')
    context = {'menu_bills': True,
               'categories': request.session['categories'],
               'bill': bill,
               'max_number': settings.MAX_NUMBER + 1,
               'number_possible_to_add': range(1, settings.MAX_NUMBER + 1),
               'products_sold': bill.reduced_sold_list(bill.produits.all()),
               # By default we add one product only
               'count': request.session.get('count', 1),
               'current_cat': category_id}
    LOG.debug("Context for categories : {0}".format(context))
    return render(request, 'bill/categories.html', context)


@login_required
def product_select_made_with(request, bill_id, product_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param product_id:
    :type product_id:
    """
    context = {'menu_bills': True,
               'bill': get_object_or_404(Facture, pk=bill_id),
               'product': get_object_or_404(ProduitVendu, pk=product_id),
               'categories': Categorie.objects.filter(made_in_kitchen=True)}
    return render(request, 'bill/product_select_made_with.html', context)


@login_required
def product_set_made_with(request, bill_id, product_id, category_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param product_id:
    :type product_id:
    :param category_id:
    :type category_id:
    """
    product = get_object_or_404(ProduitVendu, pk=product_id)
    category = get_object_or_404(Categorie, pk=category_id)
    product.made_with = category
    product.save()
    bill = get_object_or_404(Facture, pk=bill_id)
    bill.update_kitchen()
    return redirect('sold_view', bill_id, product.id)


@login_required
def subproduct_select(request, bill_id, sold_id, category_id):
    """ Select a subproduct to a product.
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param category_id:
    :type category_id:
    """
    context = {'menu_bills': True, }
    category = get_object_or_404(Categorie, pk=category_id)
    context['products'] = Produit.objects.filter(categorie=category,
                                                 actif=True)
    context['bill_id'] = bill_id
    context['sold_id'] = sold_id
    return render(request, 'bill/subproducts.html', context)


@login_required
def sold_view(request, bill_id, sold_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    """
    context = {'menu_bills': True, }
    context['bill_id'] = bill_id
    context['sold'] = get_object_or_404(ProduitVendu, pk=sold_id)
    if request.method == 'POST':
        context['note'] = NoteForm(request.POST)
        if context['note'].is_valid():
            context['note'].save()
    else:
        context['note'] = NoteForm()
    context['notes'] = Note.objects.all()
    context['options'] = Option.objects.all()
    return render(request, 'bill/sold.html', context)


@login_required
def sold_option(request, bill_id, sold_id, option_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param option_id:
    :type option_id:
    """
    set_option(sold_id, option_id)
    return redirect('sold_view', bill_id, sold_id)


@login_required
def sold_note(request, bill_id, sold_id, note_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param note_id:
    :type note_id:
    """
    sold = get_object_or_404(ProduitVendu, pk=sold_id)
    note = get_object_or_404(Note, pk=note_id)
    if note in sold.notes.all():
        sold.notes.remove(note)
    else:
        sold.notes.add(note)
    sold.save()
    return redirect('sold_view', bill_id, sold_id)


@login_required
def sold_delete(request, bill_id, sold_id):
    """ We remove a ProduitVendu on a Facture
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    sold = get_object_or_404(ProduitVendu, pk=sold_id)
    request.session["products_modified"] = bill_id
    if sold in bill.produits.all():
        LOG.debug("[%s] remove ProduitVendu(%s)" % (bill_id, sold))
        bill.produits.remove(sold)
        sold.delete()
    else:
        menus = bill.produits.filter(contient=sold)
        if menus:
            LOG.debug("[%s] remove ProduitVendu(%s) from a menu" % (
                      bill_id, sold))
            menu = menus[0]
            menu.contient.remove(sold)
            menu.save()
            sold.delete()
            return redirect("bill_sold_working", bill_id, menu.id)
    return redirect('bill_categories', bill_id)


@login_required
def subproduct_add(request, bill_id, sold_id, product_id):
    """ Add a product to a bill. If this product contains others products,
    we have to add them too.
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param product_id:
    :type product_id:
    """
    product = get_object_or_404(Produit, pk=product_id)
    sold = ProduitVendu(produit=product)
    sold.made_with = sold.produit.categorie
    sold.save()
    menu = get_object_or_404(ProduitVendu, pk=sold_id)
    menu.contient.add(sold)
    request.session['menu_id'] = menu.id
    return redirect('bill_sold_working', bill_id, sold.id)


@login_required
def sold_options(request, bill_id, sold_id, option_id=None):
    """ Choix des options à l'ajout d'un produit
    si sold.produit.options_ok

    On aura accès à la liste complète des options
    en allant dans 'sold_view'

    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param option_id:
    :type option_id:
    """
    sold = get_object_or_404(ProduitVendu, pk=sold_id)
    context = {'menu_bills': True, }
    context['sold'] = sold
    context['bill_id'] = bill_id
    context['options'] = sold.produit.options_ok.all()
    if option_id:
        set_option(sold_id, option_id)
        return redirect('sold_view', bill_id, sold_id)
    return render(request, 'bill/options.html', context)


@login_required
def sold_working(request, bill_id, sold_id):
    """ Va gérer les différents paramètres qui doivent être saisie
    sur un nouveau produit.

    request.session['menu_id'] : si présent, défini le menu

    TODO: gerer request.session['product_to_add'] et
    request.session['product_count']

    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    """
    sold = get_object_or_404(ProduitVendu, pk=sold_id)
    if sold.produit.est_un_menu():
        category = sold.get_free_categorie()
        if category:
            return redirect('subproduct_select', bill_id, sold.id,
                            category.id)
    if not sold.is_cooking_set():
        return redirect('sold_cooking', bill_id, sold.id)
    if sold.produit.options_ok.count() and not sold.options.count():
        return redirect('bill_sold_options', bill_id, sold.id)
    menu_id = request.session.get('menu_id', False)
    if menu_id:
        # il y a un menu en attente, est-il complet ?
        request.session.pop('menu_id')
        return redirect('bill_sold_working', bill_id, menu_id)
    # at this point, all is done, so are there others products?
    if request.session.get('product_to_add', False):
        product_id = request.session['product_to_add']
        try:
            product = Produit.objects.get(id=product_id)
        except Produit.DoesNotExist:
            request.session.pop('product_to_add')
        else:
            if 'product_count' in request.session.keys():
                count = int(request.session['product_count']) - 1
                if count > 1:
                    request.session['product_count'] = count
                else:
                    request.session.pop('product_to_add')
                    request.session.pop('product_count')
            return redirect('product_add', bill_id, product_id)
    return redirect('bill_categories', bill_id, sold.produit.categorie.id)


@login_required
def product_add(request, bill_id, product_id):
    """ Add a product to a bill. If this product contains others products,
    we have to add them too.

    :param request: HttpRequest request
    :param bill_id: Facture
    :param product_id: Produit
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    if not set_edition_status(request, bill):
        LOG.debug("[F%s] bill is already in edition mode" % bill_id)
        return redirect('bill_view', bill.id)
    product = get_object_or_404(Produit, pk=product_id)

    # how many products to add
    count = int(request.session.get('count', 1))
    LOG.debug("[F%s] get %d X %s" % (bill_id, count, product))
    if count > 1:
        request.session['product_to_add'] = product_id
        request.session['product_count'] = count
        request.session['count'] = 1

    sold = ProduitVendu(produit=product)
    sold.save()
    LOG.debug("[F%s] ProduitVendu(%s) created" % (bill_id, product))
    bill.add_product(sold)
    request.session["products_modified"] = bill_id
    return redirect('bill_sold_working', bill_id, sold.id)


@login_required
def sold_cooking(request, bill_id, sold_id, cooking_id=None):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param sold_id:
    :type sold_id:
    :param cooking_id:
    :type cooking_id:
    """
    context = {'menu_bills': True, }
    context['sold'] = get_object_or_404(ProduitVendu, pk=sold_id)
    context['bill_id'] = bill_id
    if cooking_id:
        cooking_set = context['sold'].is_cooking_set()
        context['sold'].set_cooking(cooking_id)
        LOG.debug("[S%s] cooking saved: %s" % (sold_id, cooking_id))
        if not cooking_set:
            LOG.debug("[%s] no cooking present" % bill_id)
            # certainement un nouveau produit donc on veut retourner
            # sur le panneau de saisie des produits
            return redirect('bill_sold_working', bill_id, context['sold'].id)
        else:
            LOG.debug("[%s] cooking replacement" % bill_id)
            return redirect('bill_view', bill_id)
    return render(request, 'bill/cooking.html', context)


@login_required
def couverts_select(request, bill_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    """
    """List of couverts for a bill"""
    context = {'menu_bills': True, }
    context['nb_couverts'] = range(43)
    context['bill_id'] = bill_id
    return render(request, 'bill/couverts.html', context)


@login_required
def couverts_set(request, bill_id, number):
    """ Set couverts of a bill
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param number:
    :type number:
    """
    context = {'menu_bills': True, }
    bill = get_object_or_404(Facture, pk=bill_id)
    bill.set_couverts(number)
    bill.save()
    return redirect("bill_view", bill_id)


@login_required
def bill_home(request):
    """Get current list of bills, and set a parameter to indicate
    long time bill without activities

    :param HttpRequest request:
    """
    request = remove_edition(request)
    context = {'menu_bills': True, }
    context['need_auto_refresh'] = 45
    context['factures'] = Facture().non_soldees()
    for bill in context['factures']:
        sec = bill.get_last_change()
        if sec > settings.CRITICAL:
            bill.alert = "alert-danger"
        elif sec > settings.WARNING:
            bill.alert = "alert-warning"
        elif sec > settings.INFO:
            bill.alert = "alert-info"
        else:
            bill.alert = "alert-success"
    context['critical'] = settings.CRITICAL
    context['warning'] = settings.WARNING
    context['info'] = settings.INFO
    context['count'] = len(context['factures'])
    return render(request, 'bill/home.html', context)


@login_required
def bill_view(request, bill_id):
    """ Get a bill.
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    """
    request = remove_edition(request)
    context = {'menu_bills': True, }
    bill = get_object_or_404(Facture, pk=bill_id)
    context['facture'] = bill
    context['products_sold'] = bill.reduced_sold_list(bill.produits.all())
    if context['facture'].est_soldee():
        messages.add_message(request, messages.ERROR,
                             _("This invoice has already been ended"))
        return redirect('bill_home')
    return render(request, 'bill/bill.html', context)


@login_required
def bill_delete(request, bill_id):
    """
    :param HttpRequest request:
    :param bill_id: a bill
    :type bill_id: Facture
    """
    order = get_object_or_404(Facture, pk=bill_id)
    context = {'menu_bills': True, 'facture': order}
    if order.paiements.count() > 0:
        messages.add_message(request, messages.ERROR,
                             _("The bill contains payments"))
        return redirect('bill_view', bill_id)
    else:
        try:
            choice = request.POST['choice']
        except KeyError:
            LOG.debug("deletion must be confirmed")
            return render(request, 'bill/delete.html', context)
        else:
            if choice == "ok":
                LOG.info("[%s] invoice deleted by %s" % (bill_id,
                                                         request.user))
                order.delete()
                messages.add_message(request, messages.SUCCESS,
                                     _("Invoice deleted"))
                return redirect('bill_home')
            else:
                return redirect('bill_view', bill_id)
        return redirect('bill_home')


@login_required
def bill_onsite(request, bill_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    """
    order = get_object_or_404(Facture, pk=bill_id)
    order.set_onsite(not order.onsite)
    order.save()
    return redirect('bill_view', bill_id)


@login_required
def bill_payment_delete(request, bill_id, payment_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param payment_id:
    :type payment_id:
    """
    payment = get_object_or_404(Paiement, pk=payment_id)
    bill = get_object_or_404(Facture, pk=bill_id)
    bill.del_payment(payment)
    return redirect('prepare_payment', bill_id)


@login_required
def bill_payment_view(request, bill_id, payment_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param payment_id:
    :type payment_id:
    """
    context = {'menu_bills': True, }
    context['bill_id'] = bill_id
    context['payment'] = get_object_or_404(Paiement, pk=payment_id)
    return render(request, 'payments/view.html', context)


@login_required
def amount_payment(request):
    """ Permet de définir le montant d'un paiement
    bill_id doit etre dans request.session

    :param HttpRequest request:
    """
    bill_id = request.session.get('bill_id', False)
    if not bill_id:
        messages.add_message(request, messages.ERROR, _("Invalid bill"))
        return redirect('bill_home')

    context = {'menu_bills': True, }
    context['bill_id'] = bill_id
    context['left'] = request.session.get('left', "0000")
    context['right'] = request.session.get('right', "00")
    return render(request, 'payments/amount.html', context)


@login_required
def amount_count(request):
    """ Le nombre de tickets pour un paiement
    :param HttpRequest request:
    """
    bill_id = request.session.get('bill_id', False)
    if not bill_id:
        messages.add_message(request, messages.ERROR, _("Invalid bill"))
        return redirect('bill_home')

    context = {'menu_bills': True, }
    context['bill_id'] = bill_id
    context['tickets_count'] = request.session.get('tickets_count', 1)
    context['range'] = range(1, 50)
    return render(request, 'payments/count.html', context)


def amount_payment_zero(request):
    """Permet d'effacer la partie gauche et droite
    :param HttpRequest request:
    """
    request.session['left'] = "0000"
    request.session['right'] = "00"
    request.session['is_left'] = True


@login_required
def amount_payment_del(request):
    """Permet d'effacer la partie gauche et droite
    :param HttpRequest request:
    """
    amount_payment_zero(request)
    return redirect("amount_payment")


@login_required
def amount_payment_right(request):
    """Permet de passer à la partie droite
    :param HttpRequest request:
    """
    request.session['is_left'] = False
    return redirect("amount_payment")


@login_required
def amount_payment_add(request, number):
    """Permet d'ajouter un chiffre au montant
    :param HttpRequest request:
    :param number:TODO
    """
    if request.session.get('init_montant', False):
        # if add a number with init_montant,
        # we should want enter a new number
        # so we del default montant
        amount_payment_zero(request)
        request.session.pop('init_montant')
    if request.session.get('is_left', True):
        key = 'left'
    else:
        key = 'right'
    value = int(request.session.get(key, 0))
    try:
        new = int(number)
    except:
        messages.add_message(request, messages.ERROR, _("Invalid number"))
    else:
        result = value * 10 + new
        tmp = "%04d" % result
        if request.session.get('is_left', True):
            # on veut seulement les 4 derniers chiffres
            request.session['left'] = tmp[-4:]
        else:
            request.session['right'] = tmp[-2:]
    return redirect("amount_payment")


@login_required
def type_payment(request, bill_id, type_id):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param type_id:
    :type type_id:
    """
    type_payment = get_object_or_404(PaiementType, pk=type_id)
    request.session['type_selected'] = type_payment
    return redirect('prepare_payment', bill_id)


@login_required
def payment_count(request, bill_id, number):
    """
    TODO
    :param HttpRequest request:
    :param bill_id:
    :type bill_id:
    :param number:
    :type number:
    """
    try:
        request.session['tickets_count'] = int(number)
    except:
        messages.add_message(request, messages.ERROR, _("Invalid number"))
        return redirect('prepare_payment', bill_id)
    else:
        return redirect('prepare_payment', bill_id)


@login_required
def save_payment(request, bill_id):
    """Enregistre le paiement
    :param HttpRequest request:
    :param bill_id:
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    if bill.in_use_by != request.user:
        messages.add_message(request, messages.ERROR, "%s %s" % (
                             _("Bill is being edited by"), request.user))
        return redirect('bill_view', bill.id)
    if request.session.get('type_selected', False):
        type_payment = request.session['type_selected']
    else:
        messages.add_message(request, messages.ERROR, _("Invalid payment"))
        return redirect('prepare_payment', bill_id)
    if not isinstance(type_payment, type(PaiementType())):
        messages.add_message(request, messages.ERROR, _("Invalid payment"))
        return redirect('prepare_payment', bill_id)
    left = request.session.get('left', "0")
    right = request.session.get('right', "0")
    montant = "%s.%s" % (left, right)
    if type_payment.fixed_value:
        count = request.session.get('tickets_count', 1)
        try:
            result = bill.add_payment(type_payment, count, montant)
        except:
            messages.add_message(request, messages.ERROR, _("Invalid payment"))
            return redirect('prepare_payment', bill_id)
    else:
        try:
            result = bill.add_payment(type_payment, montant)
        except:
            messages.add_message(request, messages.ERROR, _("Invalid payment"))
            return redirect('prepare_payment', bill_id)
    if not result:
        messages.add_message(request, messages.ERROR,
                             _("Payment could not be saved"))
        return redirect('prepare_payment', bill_id)
    cleanup_payment(request)
    if bill.est_soldee():
        messages.add_message(request, messages.SUCCESS,
                             _("This invoice has been ended"))
#        bill.used_by()
#        if "bill_in_use" in request.session.keys():
#            request.session.pop("bill_in_use")
        remove_edition(request)
        return redirect('bill_home')
    else:
        return redirect('prepare_payment', bill_id)


def init_montant(request, montant):
    """Init left/right with a montant in str
    :param HttpRequest request:
    :param montant: TODO
    """
    (left, right) = montant.split(".")
    request.session['left'] = "%04d" % int(left)
    request.session['right'] = "%02d" % int(right)
    request.session['init_montant'] = True


def set_edition_status(request, bill):
    """Only one user can add a payment or a products
    on a bill at a time.

    We use a key in request.session to update edition status
    for a bill.

    :param HttpRequest request:
    :param Facture bill:
    """
    if not bill:
        LOG.warning("We need a bill")
        return False
    if bill.in_use_by and bill.in_use_by != request.user:
        LOG.warning("[F%s] Bill already in edition mode" % bill.pk)
        messages.add_message(request, messages.ERROR,
                             "%s %s" % (_("Bill is being edited by"),
                                        request.user))
        return False
    if request.session.get('bill_in_use', None) and\
            request.session['bill_in_use'] != bill.id:
        request = remove_edition(request)
    request.session['bill_in_use'] = bill.id
    bill.used_by(request.user)
    return True


@login_required
def prepare_payment(request, bill_id):
    """ Page d'accueil pour la gestion des paiements.
    :param HttpRequest request: HttpRequest
    :param bill_id: Pk of a Facture
    """
    bill = get_object_or_404(Facture, pk=bill_id)
    if bill.est_soldee():
        messages.add_message(request, messages.ERROR, _("Nothing to pay"))
        return redirect('bill_view', bill.id)
    # on nettoie la variable
    if 'is_left' in request.session.keys():
        request.session.pop('is_left')
    if not set_edition_status(request, bill):
        return redirect('bill_view', bill.id)
    context = {'menu_bills': True, }
    context['bill_id'] = bill_id
    request.session['bill_id'] = bill_id
    context['type_payments'] = PaiementType.objects.all()
    default = PaiementType().get_default()
    if request.session.get('type_selected', False):
        context['type_selected'] = request.session['type_selected']
    else:
        if default:
            request.session['type_selected'] = default
            context['type_selected'] = default
    context['left'] = request.session.get('left', "0000")
    context['right'] = request.session.get('right', "00")
    if context['left'] == "0000" and context['right'] == "00":
        init_montant(request, u"%.2f" % bill.restant_a_payer)
        context['left'] = request.session.get('left')
        context['right'] = request.session.get('right')
    context['tickets_count'] = request.session.get('tickets_count', 1)
    context['range'] = range(1, 15)
    context['ticket_value'] = request.session.get('ticket_value', "0.0")
    context['payments'] = bill.paiements.all()
    return render(request, 'payments/home.html', context)
