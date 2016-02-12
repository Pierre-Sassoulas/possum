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
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test

from possum.base.models import Categorie, VAT, PaiementType, Facture
from possum.base.models import Printer
from possum.base.views import check_admin
from .models import Stat


LOG = logging.getLogger(__name__)

# available rapports
RAPPORTS = {'1': {'title': _("Total TTC"),
                  'name': _("Sales"), 'keys': ["total_ttc", "guests_total_ttc",
                                               "bar_total_ttc"]},
            '2': {'title': _("Bar"),
                  'name': _("Bar"), 'keys': ["bar_average", "bar_nb"]},
            '3': {'title': _("Guest"),
                  'name': _("Guest"), 'keys': ["guests_average", "guests_nb"]},
            '4': {'title': _("VAT"),
                  'name': _("VAT"), 'keys': ["_vat", ]},
            '5': {'title': _("Payments count by type"),
                  'name': _("Payments count"), 'keys': ["_payment_nb", ]},
            '6': {'title': _("Payments values by type"),
                  'name': _("Payments values"), 'keys': ["_payment_value", ]},
            '7': {'title': _("Sales amounts by category"),
                  'name': _("Amounts/category"),
                  'keys': ["_category_value", ]},
            '8': {'title': _("Number of sales by category"),
                  'name': _("Number/category"), 'keys': ["_category_nb"]},
            }


def get_series(rapport, interval, begin, end):
    """Get series to draw graphics
    :param rapport: id
    :param interval: m, d, w, y
    :param begin: datetime.date
    :param end: datetime.date
    :return: []
    """
    if rapport not in RAPPORTS:
        LOG.warning("unknown rapport id: %s" % rapport)
        return {}
    LOG.debug("rapport[%s] interval[%s] begin[%s]>end[%s]" % (rapport,
                                                              interval,
                                                              begin, end))
    series = []
    for key in RAPPORTS[rapport]['keys']:
        stats = Stat.objects.filter(interval=interval, date__gte=begin,
                                    date__lt=end)
        if key[0] == "_":
            results = {}
            for stat in stats.filter(key__endswith=key):
                if stat.key not in results:
                    LOG.debug("new key: %s" % stat.key)
                    results[stat.key] = []
                results[stat.key].append([stat.date.isoformat(),
                                          int(stat.value)])
            # reorder results
            for subkey in results.keys():
                serie = {'name': get_name(subkey), 'data': results[subkey]}
                series.append(serie)
        else:
            serie = {'name': _(key), 'data': []}
            for stat in stats.filter(key=key):
                serie['data'].append([stat.date.isoformat(), int(stat.value)])
            series.append(serie)
    LOG.debug("series: %s" % series)
    return refill(series)


def get_name(key):
    """From a key, will extract pk and object to get a name
    All key type available are:
    _vat > VAT()
    _payment_nb > PaiementType()
    _payment_value > PaiementType()
    _category_value > Categorie()
    _category_nb > Categorie()

    :param key: str, example: 2_vat or 5_payment_nb
    :return: str
    """
    LOG.debug("key: %s" % key)
    try:
        pk = key.split("_")[0]
    except:
        return _("unknown")
    name = _("unknown")
    if "_vat" in key:
        try:
            name = VAT.objects.get(pk=pk).name
        except:
            return _("unknown")
    elif "_payment_" in key:
        try:
            name = PaiementType.objects.get(pk=pk).nom
        except:
            return _("unknown")
    elif "_category_" in key:
        try:
            name = Categorie.objects.get(pk=pk).nom
        except:
            return _("unknown")
    LOG.debug("return: %s" % name)
    return name


def refill(series):
    """we need to find serie with the most date to complete others correctly,
    each series must have same count of dates.

    :param series: [{'name': key, 'data': [("2012-31-03", 3), ("1978-03-03", 2)
    :return: series refill to get proper graph
    """
    # construct template with all dates
    template = []
    for serie in series:
        for date, value in serie['data']:
            if date not in template:
                LOG.debug("new date: %s" % date)
                template.append(date)
    LOG.debug("template: %s" % template)
    # last, we need to complete all series and sort them
    for serie in series:
        # we need to add some dates
        list_dates = [date for date, value in serie['data']]
        LOG.debug("List dates of a serie: %s" % list_dates)
        for date in template:
            if date not in list_dates:
                LOG.debug("we add %s" % date)
                serie['data'].append([date, 0])
        serie['data'] = sorted(serie['data'])
        LOG.debug("new serie %s: %s" % (serie['name'], serie['data']))
    return series


@user_passes_test(check_admin)
def update(request):
    """Update statistics
    """
    if Stat().update():
        messages.add_message(request, messages.SUCCESS,
                             _("Data up to date"))
    else:
        messages.add_message(request, messages.ERROR,
                             _("Error during update"))
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
                                 _("Mail could not be sent"))
        else:
            messages.add_message(request, messages.SUCCESS,
                                 _("Mail sent to %s") % request.user.email)
    else:
        messages.add_message(request, messages.ERROR,
                             _("You have no email address"))


@user_passes_test(check_admin)
def print_msg(request, msg):
    """Print a msg to a printer
    """
    printers = Printer.objects.filter(manager=True)
    if printers:
        printer = printers[0]
        if printer.print_msg(msg):
            messages.add_message(request, messages.SUCCESS,
                                 _("Printing on %s") % printer.name)
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Printing failed on %s") %
                                 printer.name)
    else:
        messages.add_message(request, messages.ERROR,
                             _("No 'manager' printer available"))


def get_value(context, key):
    """Get value or give a default one
    """
    if key in context:
        return "%s\n" % context[key]
    else:
        return "0.00\n"


def prepare_full_output(context):
    """Prepare full output
    """
    LOG.debug(context)
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
    context = {'menu_sales': True}
    context = init_borders(context)
    context['date'] = context['last_date']
    context['interval'] = get_interval(request)
    if request.method == 'POST':
        try:
            date = datetime.datetime.strptime(request.POST.get('date'),
                                              "%Y-%m-%d").date()
        except:
            messages.add_message(request, messages.ERROR,
                                 _("Date is not valid"))
        else:
            context['date'] = date
            context = Stat().get_a_date(context)
            BETTER = ['total_ttc', 'nb_bills', 'guests_total_ttc', 'guests_nb',
                      'guests_average', 'bar_total_ttc', 'bar_nb',
                      'bar_average']
            for key in BETTER:
                LOG.debug("[%s] %s > %s ?" % (key, context[key],
                                              context['avg_%s' % key]))
                if float(context[key]) > float(context['avg_%s' % key]):
                    better = '%s_better' % key
                    context['%s_better' % key] = True
                    LOG.debug(better)
            if context['interval'] == "m":
                context['title'] = "%s: %s" % (_("Report of the month"),
                                               context['date'])
            elif context['interval'] == "w":
                context['title'] = "%s: %s" % (_("Report of the week"),
                                               context['date'])
            else:
                context['title'] = "%s: %s" % (_("Report of the day"),
                                               context['date'])
            check_for_outputs(request, context)
    else:
        context['date'] = context['last_date']
    return render(request, 'stats/home.html', context)


def init_borders(context):
    """
    Get date of first and last order to limit datepicker choice.
    """
    first_order = Facture.objects.first()
    if first_order:
        context['first_date'] = first_order.date_creation.date().isoformat()
    else:
        context['first_date'] = datetime.date.today().isoformat()
    last_order = Facture.objects.last()
    if last_order:
        context['last_date'] = last_order.date_creation.date().isoformat()
    else:
        context['last_date'] = context['first_date']
    LOG.debug("interval: %s --> %s" % (context['first_date'],
                                       context['last_date']))
    return context


def get_interval(request):
    """Extract and test interval from a form.
    Default value is: day
    """
    if request.method == 'POST':
        rapport = request.POST.get('interval')
        if rapport == "m":
            LOG.debug("m")
            return "m"
        elif rapport == "w":
            LOG.debug("w")
            return "w"
        elif rapport == "y":
            LOG.debug("y")
            return "y"
    # default value
    LOG.debug("d")
    return "d"


@user_passes_test(check_admin)
def charts(request):
    """Show graphics
    """
    context = {'menu_sales': True, 'rapport': '1'}
    context = init_borders(context)
    context['cat_list'] = Categorie.objects.order_by('priorite', 'nom')
    context['interval'] = get_interval(request)
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
    return render(request, 'stats/charts.html', context)


@user_passes_test(check_admin)
def dump(request, rapport, interval, date_begin, date_end):
    """Get stats for graphics
    All tests on data are made in Stat()
    """
    LOG.debug(rapport)
    data = {}
    try:
        begin = datetime.datetime.strptime(date_begin, "%Y-%m-%d").date()
    except:
        begin = None
    try:
        end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
    except:
        end = None
    if begin and end:
        data['chart_data'] = get_series(rapport, interval, begin, end)
    else:
        data['chart_data'] = {}
    return HttpResponse(json.dumps(data), content_type='application/json')
