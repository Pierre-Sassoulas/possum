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
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test

from possum.base.models import Categorie, Config, Printer, Produit, VAT
from possum.base.views import check_admin
from possum.stats.models import Stat


LOG = logging.getLogger(__name__)


@user_passes_test(check_admin)
def categories_send(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    result = Produit().get_list_with_all_products()
    subject = _("Carte")
    mail = ""
    for line in result:
        mail += "%s\n" % line
    if request.user.email:
        try:
            send_mail(subject, mail, settings.DEFAULT_FROM_EMAIL,
                      [request.user.email], fail_silently=False)
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Message could not be sent"))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 _("Message was sent to %s")
                                 % request.user.email)
    else:
        messages.add_message(request, messages.ERROR,
                             _("You have no email address"))
    return redirect('categories')


@user_passes_test(check_admin)
def categories_print(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    result = Produit().get_list_with_all_products()
    if result:
        printers = Printer.objects.filter(manager=True)
        if printers:
            printer = printers[0]
            if printer.print_list(result, "carte_complete"):
                messages.add_message(request, messages.SUCCESS,
                                     _("Printing was sent to %s") %
                                     printer.name)
            else:
                messages.add_message(request, messages.ERROR,
                                     _("Printing has failed on %s")
                                     % printer.name)
        else:
            messages.add_message(request, messages.ERROR,
                                 _("No printers 'manager' available"))
    else:
        messages.add_message(request, messages.ERROR, _("No product"))
    return redirect('categories')


@user_passes_test(check_admin)
def categories(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context['categories'] = Categorie.objects.order_by('priorite', 'nom')
    return render(request, 'manager/carte/categorie_list.html', context)


@user_passes_test(check_admin)
def categories_delete(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['current_cat'] = get_object_or_404(Categorie, pk=category_id)
    context['categories'] = Categorie.objects.order_by('priorite',
                                                       'nom').exclude(id=category_id)
    cat_report_id = request.POST.get('cat_report', '').strip()
    action = request.POST.get('valide', '').strip()
    if action == "remove":
        products_list = Produit.objects.filter(categorie__id=category_id)
        # we have to report stats and products ?
        if cat_report_id:
            try:
                report = Categorie.objects.get(id=cat_report_id)
                # we transfer all products
                for product in products_list:
                    product.categorie = report
                    product.save()
            except Categorie.DoesNotExist:
                LOG.warning("[%s] category [%s] doesn't exist" % (
                            request.user.username, cat_report_id))
                messages.add_message(request, messages.ERROR,
                                     _("Category does not exist"))
                return redirect('categories_delete', category_id)
            report_info = "from [%s] to [%s]" % (context['current_cat'],
                                                 report)
            LOG.info("move stats %s" % report_info)
            for key in ["category_nb", "category_value"]:
                new_key = "%s_%" % (cat_report_id, key)
                for s in Stat.objects.filter(key="%s_%s" % (category_id, key)):
                    new, created = Stat.objects.get_or_create(key=new_key,
                                                              year=s.year,
                                                              month=s.month,
                                                              week=s.week,
                                                              day=s.day,
                                                              interval=s.interval)
                    new.add_value(s.value)
                    s.delete()
            LOG.info("copy products %s" % report_info)
            for product in products_list:
                new = product._clone_product()
                new.categorie = report
                new.update_vats(keep_clone=False)
                new.save()
        if products_list.count() == 0:
            context['current_cat'].delete()
            LOG.info("[%s] category [%s] deleted" % (request.user.username,
                     context['current_cat'].nom))
            return redirect('categories')
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Category contains products, "
                                   "deletion canceled"))

    elif action == "cancel":
        return redirect('categories')
    return render(request, 'manager/carte/categorie_delete.html', context)


@user_passes_test(check_admin)
def categories_view(request, category_id):
    '''
    :param request:
    :type request:
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    products = Produit.objects.filter(categorie__id=category_id)
    context['products_enable'] = products.filter(actif=True)
    context['products_disable'] = products.filter(actif=False)
    return render(request, 'manager/carte/categorie_detail.html', context)


@user_passes_test(check_admin)
def categories_add(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    return render(request, 'base/carte/categories_add.html', context)


@user_passes_test(check_admin)
def categories_new(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    priority = request.POST.get('priority', '').strip()
    name = request.POST.get('name', '').strip()
    if name:
        cat = Categorie()
        cat.nom = name
        if priority:
            cat.priorite = priority
        try:
            cat.save()
            LOG.info("[%s] new categorie [%s]" % (request.user.username, name))
        except:
            LOG.warning("[%s] new categorie failed: [%s] [%s]" % (
                        request.user.username, cat.priorite, cat.nom))
            messages.add_message(request, messages.ERROR,
                                 _("New category has not been created"))
    else:
        messages.add_message(request, messages.ERROR,
                             _("You must choose a name for the new category"))
    return redirect('categories')


@user_passes_test(check_admin)
def categories_name(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    return render(request, 'manager/carte/categorie_name.html', context)


@user_passes_test(check_admin)
def categories_color(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    context['categories'] = Categorie.objects.order_by('priorite', 'nom')
    return render(request, 'manager/carte/categorie_color.html', context)


@user_passes_test(check_admin)
def categories_less_priority(request, category_id, nb=1):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    :param nb:
    :type nb:
    '''
    cat = get_object_or_404(Categorie, pk=category_id)
    cat.set_less_priority(nb)
    LOG.info("[%s] cat [%s] priority - %d" % (request.user.username, cat.nom,
                                              nb))
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_more_priority(request, category_id, nb=1):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    :param nb:
    :type nb:
    '''
    cat = get_object_or_404(Categorie, pk=category_id)
    cat.set_more_priority(nb)
    LOG.info("[%s] cat [%s] priority + %d" % (request.user.username, cat.nom,
                                              nb))
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_surtaxable(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    cat = get_object_or_404(Categorie, pk=category_id)
    new = not cat.surtaxable
    cat.surtaxable = new
    if cat.surtaxable:
        cat.disable_surtaxe = False
    cat.save()
    for product in Produit.objects.filter(categorie=cat).iterator():
        product.update_vats()
    LOG.info("[%s] cat [%s] surtaxable: %s" % (request.user.username,
                                               cat.nom, cat.surtaxable))
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_vat_takeaway(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    context['type_vat'] = _("VAT take away")
    request.session['vat'] = 'vat_takeaway'
    context['vats'] = VAT.objects.order_by('name')
    return render(request, 'manager/carte/select_vat.html', context)


@user_passes_test(check_admin)
def categories_vat_onsite(request, category_id):
    '''
    :param HttpRequest request:
    :param category_id:
    :type category_id:
    '''
    context = {'menu_manager': True, }
    context['category'] = get_object_or_404(Categorie, pk=category_id)
    context['type_vat'] = _("VAT on site")
    request.session['vat'] = 'vat_onsite'
    context['vats'] = VAT.objects.order_by('name')
    return render(request, 'manager/carte/select_vat.html', context)


@user_passes_test(check_admin)
def categories_set_vat(request, category_id, vat_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    :param vat_id:
    :type vat_id:
    '''
    category = get_object_or_404(Categorie, pk=category_id)
    vat = get_object_or_404(VAT, pk=vat_id)
    type_vat = request.session.get('vat', "")
    if type_vat:
        if type_vat == 'vat_onsite':
            LOG.debug("[%s] new vat onsite" % category)
            category.set_vat_onsite(vat)
        else:
            LOG.debug("[%s] new vat takeaway" % category)
            category.set_vat_takeaway(vat)
        del request.session['vat']
        for product in Produit.objects.filter(categorie=category,
                                              actif=True).iterator():
            product.update_vats()
    else:
        messages.add_message(request, messages.ERROR,
                             _("VAT type not defined"))
    return redirect('categories_view', category_id)


def update_colors():
    """Create/update a css file with all categories color
    """
    try:
        fd = open(settings.CAT_CSS, "w")
    except:
        LOG.warning("Can't open file: %s" % settings.CAT_CSS)
    else:
        fd.write("/* Auto generate file, do not update by hand */\n")
        for cat in Categorie.objects.iterator():
            if cat.color:
                fd.write(".cat_%s {background:%s;}\n" % (cat.id, cat.color))
        fd.close()
        LOG.info("CSS for categories colors updated")


@user_passes_test(check_admin)
def categories_set_color(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    color = request.POST.get('color', '').strip()
    cat = get_object_or_404(Categorie, pk=category_id)
    if not cat.color or color != cat.color:
        LOG.info("[%s] new categorie color [%s]" % (request.user.username,
                                                    cat.nom))
        cat.color = color
        try:
            cat.save()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Changes could not be saved"))
        else:
            update_colors()
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_set_name(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    name = request.POST.get('name', '').strip()
    cat = get_object_or_404(Categorie, pk=category_id)
    if name != cat.nom:
        LOG.info("[%s] new categorie name: [%s] > [%s]" % (
                    request.user.username, cat.nom, name))
        cat.nom = name
    try:
        cat.save()
    except:
        messages.add_message(request, messages.ERROR,
                             _("Changes could not be saved"))
        LOG.warning("[%s] save failed for [%s]" % (
                       request.user.username, cat.nom))
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_set_default(request, category_id):
    """Set a default category
    """
    config, created = Config.objects.get_or_create(key="category_default")
    config.value = category_id
    config.save()
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_set_kitchen(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    cat = get_object_or_404(Categorie, pk=category_id)
    new = not cat.made_in_kitchen
    cat.made_in_kitchen = new
    cat.save()
    return redirect('categories_view', category_id)


@user_passes_test(check_admin)
def categories_disable_surtaxe(request, category_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param category_id:
    :type category_id:
    '''
    cat = get_object_or_404(Categorie, pk=category_id)
    new = not cat.disable_surtaxe
    cat.disable_surtaxe = new
    if cat.disable_surtaxe:
        cat.surtaxable = False
    cat.save()
    return redirect('categories_view', category_id)
