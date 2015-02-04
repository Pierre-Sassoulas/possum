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
import json

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test

from possum.base.forms import DateForm
from possum.base.models import Categorie, VAT, PaiementType, Produit, Facture
from possum.base.models import Printer
from possum.base.views import check_admin
from possum.stats.models import Stat, STATS, RAPPORTS


LOGGER = logging.getLogger(__name__)


@user_passes_test(check_admin)
def update(request):
    """Update statistics
    """
    if Stat().update():
        messages.add_message(request, messages.SUCCESS,
                             "Les données sont à jour")
    else:
        messages.add_message(request, messages.ERROR,
                             "Les données ne peuvent être mis à jour")
    return redirect("sales_home")


@user_passes_test(check_admin)
def send(request, subject, message):
    """Send an email
    """
    if request.user.email:
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      [request.user.email], fail_silently=False)
        except:
            messages.add_message(request, messages.ERROR,
                                 u"Le mail n'a pu être envoyé")
        else:
            messages.add_message(request, messages.SUCCESS,
                                 u"Mail envoyé à %s" % request.user.email)
    else:
        messages.add_message(request, messages.ERROR,
                             u"Vous n'avez pas d'adresse mail")


@user_passes_test(check_admin)
def print_msg(request, msg):
    """Print a msg to a printer
    """
    printers = Printer.objects.filter(manager=True)
    if printers:
        printer = printers[0]
        if printer.print_msg(msg):
            messages.add_message(request, messages.SUCCESS,
                                 u"L'impression a été envoyée sur %s" %
                                 printer.name)
        else:
            messages.add_message(request, messages.ERROR,
                                 u"L'impression a échouée sur %s" %
                                 printer.name)
    else:
        messages.add_message(request, messages.ERROR,
                             u"Aucune imprimante type 'manager' disponible")


@user_passes_test(check_admin)
def get_value(context, key):
    """Get value or give a default one
    """
    if key in context:
        return "%s\n" % context[key]
    else:
        return "0.00\n"


@user_passes_test(check_admin)
def prepare_full_output(context):
    """Prepare full output
    """
    LOGGER.debug(context)
    msg = """
Nb factures: """
    msg += get_value(context, 'nb_bills')
    msg += prepare_vats_output(context)
    msg += """
Restauration:
Nb couverts: """
    msg += get_value(context, 'guests_nb')
    msg += "Total TTC: "
    msg += get_value(context, 'guests_total_ttc')
    msg += "TM/couvert: "
    msg += get_value(context, 'guests_average')
    msg += """
Bar:
Nb factures: """
    msg += get_value(context, 'bar_nb')
    msg += "Total TTC: "
    msg += get_value(context, 'bar_total_ttc')
    msg += "TM/facture: "
    msg += get_value(context, 'bar_average')
    msg += "\n"
    if 'payments' in context:
        for payment in context['payments']:
            msg += "%s: %.2f\n" % (payment, payment.nb)
    msg += "\n"
    if 'categories' in context:
        for category in context['categories']:
            msg += "%s: %s\n" % (category.nom, category.nb)
    msg += "\n"
    if 'products' in context:
        for product in context['products']:
            msg += "%s: %s\n" % (product.nom, product.nb)
    msg += "\nFait le %s" % datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    return msg


@user_passes_test(check_admin)
def prepare_vats_output(context):
    """Prepare VATS output
    """
    msg = "Total TTC: "
    msg += get_value(context, 'total_ttc')
    if 'vats' in context:
        for vat in context['vats']:
            msg += "TTC %s: %.2f\n" % (vat, vat.nb)
    return msg


@user_passes_test(check_admin)
def check_for_outputs(request, context):
    """Check if user wants some outputs
    """
    if context and request.method == 'POST':
        if "full_mail" in request.POST:
            subject = context['title']
            msg = prepare_full_output(context)
            send(request, subject, msg)
        if "full_print" in request.POST:
            msg = context['title']
            msg += prepare_full_output(context)
            print_msg(request, msg)
        if "vats_mail" in request.POST:
            subject = context['title']
            msg = prepare_vats_output(context)
            send(request, subject, msg)
        if "vats_print" in request.POST:
            msg = context['title']
            msg += prepare_vats_output(context)
            print_msg(request, msg)


@user_passes_test(check_admin)
def text(request):
    """Show stats
    """
    context = {'menu_sales': True, 'date': datetime.datetime.now()}
    context = init_borders(context)
    context['interval'] = get_rapport_type(request)
    if request.method == 'POST':
        try:
            date = datetime.datetime.strptime(request.POST.get('date'),
                                              "%d-%m-%Y")
        except:
            messages.add_message(request,
                                 messages.ERROR,
                                 "La date saisie n'est pas valide.")
        else:
            context['date'] = date
            if context['interval'] == "m":
                context['title'] = "%s: %s" % (_("Report of the month"),
                                               date.strftime("%m/%Y"))
                context = Stat().get_data_for_month(context)
            elif context['interval'] == "w":
                context['title'] = "%s: %d %s" % (_("Report of the week"),
                                                  date.year,
                                                  date.isocalendar()[1])
                context = Stat().get_data_for_week(context)
            else:
                context['interval'] = "d"
                context['title'] = "%s: %s" % (_("Report of the day"),
                                               date.strftime("%d/%m/%Y"))
                context = Stat().get_data_for_day(context)
            check_for_outputs(request, context)
    return render(request, 'stats/home.html', context)


def month_name(*t):
    """ Sert à trier les mois."""
    names = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Jui',
             7: 'Jui', 8: 'Aou', 9: 'Sep', 10: 'Oct', 11: 'Nov',
             12: 'Dec'}
    month_num = int(t[0][0])
    LOGGER.debug("names[%d] > [%s]" % (month_num, names[month_num]))
    return (names[month_num],)


def month_sort(*x):
    """x example: ((('Fev',), ('2',)),)
    """
    return (int(x[0][1][0]),)


def get_chart_year_products(year, category):
    charts = []
    keys_nb = {}
    keys_value = {}
    for product in Produit.objects.filter(categorie=category).iterator():
        name = "%s #%s" % (product.nom, product.id)
        key = "%s_product_nb" % product.id
        keys_nb[key] = name
        key = "%s_product_value" % product.id
        keys_value[key] = name
    try:
        datasource = get_datapool_year(year, keys_nb)
    except:
        return False
    title = u"Nombre de vente pour la catégorie [%s] en %s" % (category.nom,
                                                               year)
    charts.append(get_chart(datasource, 'line', keys_nb, title, "Mois"))
    try:
        datasource = get_datapool_year(year, keys_value)
    except:
        return False
    title = u"Valeur des ventes pour la catégorie [%s] en %s" % (category.nom,
                                                                 year)
    charts.append(get_chart(datasource, 'line', keys_value, title, "Mois"))
    return charts


@user_passes_test(check_admin)
def select_charts(request, context):
    """Select and construct graphics
    """
    charts = []
    choice = context['choice']
    year = 2015
    if choice == 'ttc':
        title = "Total TTC pour l'année %d" % year
        chart = {'title': title, }
        context['title'] = title
        chart['keys'] = {"total_ttc": 'total ttc',
                         "guests_total_ttc": 'restauration',
                         "bar_total_ttc": 'bar'}
        charts.append(chart)
    elif choice == 'bar':
        chart = {'title': "Activité bar pour l'année %d" % year, }
        chart['keys'] = {"bar_average": 'TM/facture',
                         "bar_nb": 'nb factures'}
        charts.append(chart)
    elif choice == 'guests':
        chart = {'title': "Activité restaurant pour l'année %d" % year, }
        chart['keys'] = {"guests_average": 'TM/couvert',
                         "guests_nb": 'nb couverts'}
        charts.append(chart)
    elif choice == 'vats':
        chart = {'title': "TTC des TVA pour l'année %d" % year, }
        chart['keys'] = {}
        for vat in VAT.objects.iterator():
            key = "%s_vat" % vat.id
            chart['keys'][key] = "%s" % vat
        charts.append(chart)
    elif choice == 'payments':
        chart1 = {'title': "Nombre de paiements par type pour l'année %d" %
                  year, }
        chart1['keys'] = {}
        chart2 = {'title': "Valeur des paiements par type pour l'année %d" %
                  year, }
        chart2['keys'] = {}
        for payment in PaiementType.objects.iterator():
            key = "%s_payment_nb" % payment.id
            chart1['keys'][key] = payment.nom
            key = "%s_payment_value" % payment.id
            chart2['keys'][key] = payment.nom
        charts.append(chart1)
        charts.append(chart2)
    elif choice == 'categories':
        chart1 = {'title': "Nombre de vente par catégorie pour l'année %d" %
                  year, }
        chart1['keys'] = {}
        chart2 = {'title': "Valeur des ventes par catégorie pour l'année %d" %
                  year, }
        chart2['keys'] = {}
        for cat in Categorie.objects.iterator():
            key = "%s_category_nb" % cat.id
            chart1['keys'][key] = cat.nom
            key = "%s_category_value" % cat.id
            chart2['keys'][key] = cat.nom
        charts.append(chart1)
        charts.append(chart2)
    else:
        try:
            category = Categorie.objects.get(pk=choice)
        except:
            messages.add_message(request, messages.ERROR,
                                 "Ce type de graphique n'existe pas.")
        else:
            chart1 = {'title': u"Nombre de vente pour la catégorie [%s] en %d"
                      % (category.nom, year), }
            chart1['keys'] = {}
            chart2 = {'title': u"Valeur des ventes pour la catégorie [%s] en "
                      "%d" % (category.nom, year), }
            chart2['keys'] = {}
            for product in Produit.objects.filter(categorie=category):
                name = "%s #%s" % (product.nom, product.id)
                key = "%s_product_nb" % product.id
                chart1['keys'][key] = name
                key = "%s_product_value" % product.id
                chart2['keys'][key] = name
            charts.append(chart1)
            charts.append(chart2)
    # if one chart, it is in context['chart1'] = chart
    # else, if two charts: context['chart2'] = [chart1, chart2]
    key = 'chart%d' % len(charts)
    context[key] = []
    for chart in charts:
        try:
            datasource = get_datapool_year(year, chart['keys'])
        except:
            LOGGER.warning("datasource error with %s" % chart['title'])
        else:
            context[key].append(get_chart(datasource, 'line',
                                          chart['keys'],
                                          chart['title'],
                                          "Mois"))
    return context


def init_borders(context):
    """Get date of first and last order to limit datepicker choice.
    """
    first_order = Facture.objects.first()
    if first_order:
        context['first_date'] = first_order.date_creation.strftime("%d-%m-%Y")
    else:
        context['first_date'] = datetime.datetime.now().strftime("%d-%m-%Y")
    last_order = Facture.objects.last()
    if last_order:
        context['last_date'] = last_order.date_creation.strftime("%d-%m-%Y")
    else:
        context['last_date'] = context['first_date']
    LOGGER.warning("interval: %s > %s" % (context['first_date'],
                                          context['last_date']))
    return context


def get_rapport_type(request):
    """Extract and test rapport type from a form.
    Default value is: day
    """
    if request.method == 'POST':
        rapport = request.POST.get('interval')
        if rapport == "m":
            return "m"
        elif rapport == "w":
            return "w"
        elif rapport == "y":
            return "y"
    # default value
    return "d"


@user_passes_test(check_admin)
def charts(request):
    """Show graphics
    """
    context = {'menu_sales': True, 'rapport': '1'}
    context = init_borders(context)
    context['cat_list'] = Categorie.objects.order_by('priorite', 'nom')
    context['interval'] = get_rapport_type(request)
    context['date_begin'] = context['first_date']
    context['date_end'] = context['last_date']
    context['rapports'] = RAPPORTS
    if request.method == 'POST':
        if 'date_begin' in request.POST:
            context['date_begin'] = request.POST.get('date_begin')
        if 'date_end' in request.POST:
            context['date_end'] = request.POST.get('date_end')
        context['rapport'] = request.POST.get('rapport')
    context['title'] = RAPPORTS[context['rapport']]['title']
#    context = select_charts(request, context)
    return render(request, 'stats/charts.html', context)


@user_passes_test(check_admin)
def dump(request, rapport, interval, date_begin, date_end):
    """Get stats for graphics
    All tests on data are made in Stat()
    """
    data = {}
    data['chart_data'] = Stat().test_get_chart(rapport, interval, date_begin, date_end)
    return HttpResponse(json.dumps(data), content_type='application/json')
