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
from decimal import Decimal
import itertools
import logging
import os

from django.conf import settings
from django.db import models
from django.db.models import Max, Avg

from possum.base.models import Categorie
from possum.base.models import Facture
from possum.base.models import PaiementType
from possum.base.models import Produit
from possum.base.models import VAT


LOG = logging.getLogger(__name__)
# availables stats and keys
STATS = ["total_ttc", "nb_bills", "guests_total_ttc", "guests_nb",
         "guests_average", "bar_total_ttc", "bar_nb", "bar_average"]


def get_month(date):
    """
    date: datetime
    Return datetime.date() for a month
    """
    return datetime.date(date.year, date.month, 1)


def get_year(date):
    """
    date: datetime
    Return datetime.date() for a year
    """
    return datetime.date(date.year, 1, 1)


def get_week(date):
    """
    date: datetime
    Return datetime.date() for a week
    First day of week is monday
    """
    if date.weekday() == 0:
        return date + datetime.timedelta(days=1)
    elif date.weekday() > 1:
        nb_days = date.weekday() - 1
        return date - datetime.timedelta(days=nb_days)
    else:
        return date


def find_right_date(date, interval):
    """Select rhe right date,
    If interval is month, it is first day of month
    if intervak is year, it is first day of year
    if interval is week, it is monday
    :param date: datetime.date()
    :param interval: 'm'
    :return: dateteime.date()
    """
    if interval == "m":
        return get_month(date)
    elif interval == "y":
        return get_year(date)
    elif interval == "w":
        return get_week(date)
    else:
        return date


def get_last_year(date, interval):
    """Get lat year date

    :param date: current date
    :param interval: which interval (d, m, w or y)
    :return: datetime.date
    """
    if interval == "y" or interval == "m":
        # year - 1
        return datetime.date(date.year - 1, date.month, date.day)
    else:
        return date - datetime.timedelta(weeks=52)


def get_data_from(bill, data):
    """Extract data on a bill to add it to the stats

    bill: Facture()
    data: {}
    """
    def add_value(key, value):
        if key in data.keys():
            data[key] += Decimal(value)
        else:
            data[key] = Decimal(value)
        LOG.debug("%s = %.2f" % (key, data[key]))
    LOG.debug("[B%s] extract stats" % bill.id)
    add_value("nb_bills", 1)
    add_value("total_ttc", bill.total_ttc)
    for sold in bill.produits.iterator():
        prix = sold.prix
        p_id = sold.produit.id
        add_value("%s_product_nb" % p_id, 1)
        add_value("%s_product_value" % p_id, prix)
        c_id = sold.produit.categorie_id
        add_value("%s_category_nb" % c_id, 1)
        add_value("%s_category_value" % c_id, prix)
        # VAT
        if bill.onsite:
            vat_id = sold.produit.categorie.vat_onsite_id
        else:
            vat_id = sold.produit.categorie.vat_takeaway_id
        add_value("%s_vat" % vat_id, prix)
        # products in a menu
        for sub in sold.contient.iterator():
            p_id = sub.produit.id
            add_value("%s_product_nb" % p_id, 1)
            c_id = sub.produit.categorie_id
            add_value("%s_category_nb" % c_id, 1)
    if bill.est_un_repas():
        # number of guests
        if bill.couverts == 0:
            # if not, we try to find a number
            bill.couverts = bill.guest_couverts()
            bill.save()
        add_value("guests_nb", bill.couverts)
        add_value("guests_total_ttc", bill.total_ttc)
    else:
        add_value("bar_nb", 1)
        add_value("bar_total_ttc", bill.total_ttc)
    for payment in bill.paiements.iterator():
        p_id = payment.type_id
        add_value("%s_payment_nb" % p_id, 1)
        add_value("%s_payment_value" % p_id, payment.montant)
    return data


def _search_sub_key(stats, key, a_class, integer=False):
    """
    :param stats: Stat.object.filter()
    :param key: string, subkey to search
    :param a_class: a class of object to find
    :param integer: output values must be an integer or a float
    :return: []
    """
    tmp = []
    for stat in stats.filter(key__contains=key):
        pk = stat.key.split("_")[0]
        try:
            elt = a_class.objects.get(pk=pk)
        except:
            LOG.critical("[%s] pk=%s not here" % (key, pk))
        else:
            if integer:
                elt.nb = int(stat.value)
            else:
                elt.nb = stat.value
            tmp.append(elt)
    LOG.debug(tmp)
    return sorted(tmp, key=lambda stat: stat.nb, reverse=True)


def compute_avg_max(stats, stat_avg, stat_max):
    """Get and save maximum and average for all stats
    stats: Stat.objects.filter()
    stat_avg: Stat()
    stat_max: Stat()
    """
    avg = stats.aggregate(Avg('value'))['value__avg']
    if avg:
        stat_avg.value = avg
        stat_avg.save()
        LOG.debug("new average: %.2f" % avg)
    best = stats.aggregate(Max('value'))['value__max']
    if best:
        stat_max.value = best
        stat_max.save()
        LOG.debug("new best: %.2f" % best)


def compute_all_time():
    """Update all time stats (average and max) for main keys
    """
    LOG.debug("update all time stats")
    for key in STATS:
        LOG.debug("days(a)")
        stats = Stat.objects.filter(interval="d", key=key)
        avg, created = Stat.objects.get_or_create(interval="a",
                                                  key="avg_%s" % key)
        best, created = Stat.objects.get_or_create(interval="a",
                                                   key="max_%s" % key)
        compute_avg_max(stats, avg, best)
        LOG.debug("months(b)")
        stats = Stat.objects.filter(interval="m", key=key)
        avg, created = Stat.objects.get_or_create(interval="b",
                                                  key="avg_%s" % key)
        best, created = Stat.objects.get_or_create(interval="b",
                                                   key="max_%s" % key)
        compute_avg_max(stats, avg, best)
        LOG.debug("weeks(c)")
        stats = Stat.objects.filter(interval="w", key=key)
        avg, created = Stat.objects.get_or_create(interval="c",
                                                  key="avg_%s" % key)
        best, created = Stat.objects.get_or_create(interval="c",
                                                   key="max_%s" % key)
        compute_avg_max(stats, avg, best)


def record_day(date, data):
    """Record new values from data.
    Also update average, max.

    date: datetime
    data: {'key1': value1, 'key2': value2, ...}
    """
    LOG.debug("[%s] update record" % date.isoformat())
    for key in data.keys():
        stat, created = Stat.objects.get_or_create(date=date, key=key,
                                                   interval="d")
        stat.add_value(data[key])
        stat, created = Stat.objects.get_or_create(date=get_month(date),
                                                   key=key, interval="m")
        stat.add_value(data[key])
        stat, created = Stat.objects.get_or_create(date=get_week(date),
                                                   key=key, interval="w")
        stat.add_value(data[key])
        stat, created = Stat.objects.get_or_create(date=get_year(date),
                                                   key=key, interval="y")
        stat.add_value(data[key])


def compute_avg(subkey, stats, avg):
    """Compute average
    subkey: "guests" or "bar"
    stats: Stat.objects.filter()
    avg: Stat()
    """
    LOG.debug(subkey)
    try:
        total = stats.filter(key="%s_total_ttc" % subkey)[0]
        nb = stats.filter(key="%s_nb" % subkey)[0]
    except IndexError:
        LOG.debug("no data for this date")
        # if no data here, no need to update month and week
        return False
    if nb.value:
        avg.value = total.value / nb.value
        avg.save()
    else:
        LOG.debug("we don't divide by zero")
        return False
    return True


def update_avg(date):
    """Update average/max stats for day, week and month

    guests_average = guests_total_ttc.value / guests_nb.value
    bar_average = bar_total_ttc.value / bar_nb.value
    """
    LOG.debug("update guests_average and bar_average")
    for key in ["guests", "bar"]:
        stats = Stat.objects.filter(date=date, interval="d")
        avg, created = Stat.objects.get_or_create(date=date, interval="d",
                                                  key="%s_average" % key)
        if compute_avg(key, stats, avg):
            month = get_month(date)
            stats = Stat.objects.filter(date=month, interval="m")
            avg, created = Stat.objects.get_or_create(date=month,
                                                      key="%s_average" % key,
                                                      interval="m")
            compute_avg(key, stats, avg)
            week = get_week(date)
            stats = Stat.objects.filter(date=week, interval="w")
            avg, created = Stat.objects.get_or_create(date=week, interval="w",
                                                      key="%s_average" % key)
            compute_avg(key, stats, avg)


def update_day(date):
    """Update stats with all bills availables on a day.

    date: datetime.date
    """
    end = date + datetime.timedelta(days=1)
    bills = Facture.objects.filter(date_creation__gte=date,
                                   date_creation__lt=end)\
        .exclude(saved_in_stats=True)
    data = {}
    count = 0
    LOG.debug("[%s] %d bills to update" % (date, bills.count()))
    for bill in bills:
        if bill.est_soldee():
            count += 1
            data = get_data_from(bill, data)
            bill.saved_in_stats = True
            bill.save()
    if data:
        record_day(date, data)
        update_avg(date)
    else:
        LOG.debug("nothing to do")
    logging.info("updated record with %d bills" % count)
    return True


class Stat(models.Model):
    """Statistics, full list of keys:
    Common:
    nb_bills      : number of invoices
    total_ttc        : total TTC
    ID_vat           : total TTC for vat ID

    Products:
    ID_product_nb    : how many product
    ID_product_value : total TTC for product ID
    ID_category_nb   : how many product sold in category ID
    ID_category_value: total TTC for category ID

    Restaurant:
    guests_nb        : how many people
    guests_average   : average TTC by guest
    guests_total_ttc : total TTC for guests

    Bar:
    bar_total_ttc    : total TTC for bar activity
    bar_nb           : how many invoices
    bar_average      : average TTC by invoice

    Payments:
    ID_payment_nb    : number of payment ID
    ID_payment_value : total for payment ID

    All time stats are use to record average/max
    """
    INTERVAL = (('a', 'All time day'),
                ('b', 'All time month'),
                ('c', 'All time week'),
                ('y', 'Year'),
                ('w', 'Week'),
                ('m', 'Month'),
                ('d', 'Day'))
    interval = models.CharField(max_length=1, choices=INTERVAL, default="d")
    date = models.DateField(default="1978-03-03")
    # TODO: since version 0.6: year, month, week and day deprecated,
    # must be removed in version 0.7
    year = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    day = models.PositiveIntegerField(default=0)
    week = models.PositiveIntegerField(default=0)
    # END TODO
    key = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    class Meta:
        ordering = ['interval', 'date', 'key']

    def __str__(self):
        """Representing the date in ISO 8601 format, ‘YYYY-MM-DD’
        """
        date = self.date.isoformat()
        return "%s %s" % (self.interval, date)

    def update(self):
        """Update statistics with new bills
        """
        # TODO: knee knee knee .. for what ? I don't remender :(
        if os.path.isfile(settings.LOCK_STATS):
            LOG.info("lock [%s] already here" % settings.LOCK_STATS)
            return False
        else:
            LOG.debug("create lock for stats")
            fd = open(settings.LOCK_STATS, "w")
            fd.close()
            # we prepare list of days with bills to add
            bills = Facture.objects.filter(saved_in_stats=False)
            grouped = itertools.groupby(bills, lambda record:
                                        record.date_creation.date())
            for day, bills_this_day in grouped:
                update_day(day)
            if grouped:
                compute_all_time()
            LOG.debug("release lock for stats")
            os.remove(settings.LOCK_STATS)
            return True

    def add_value(self, value):
        """Add a value to the stat.

        value -- a float or string with a number"""
        try:
            self.value += Decimal(value)
        except:
            LOG.critical("can't convert [%s]" % value)
        self.save()

    def get_a_date(self, context):
        """Get Stats for a date
        This function will not test with context['date'] is a datetime.date()

        :param context: {'date': datetime.date(), 'interval': 'm'}
        :return: context with stats for context['date']
        """
        if 'date' not in context or 'interval' not in context:
            LOG.warning("No date or no interval in context")
            return context
        date = find_right_date(context['date'], context['interval'])
        if context['interval'] == "m":
            alltime_interval = "b"
        elif context['interval'] == "w":
            alltime_interval = "c"
        else:
            alltime_interval = "a"
        stats = Stat.objects.filter(interval=context['interval'], date=date)
        for key in STATS:
            try:
                value = "%.2f" % stats.get(key=key).value
            except:
                LOG.debug("[%s][%s][%s] missing" % (date, context['interval'],
                                                    key))
                value = "0.00"
            context[key] = value
            # maximum and average
            for i in ['max_', 'avg_']:
                tmp = "%s%s" % (i, key)
                try:
                    get = Stat.objects.get
                    value = "%.2f" % get(interval=alltime_interval,
                                         key=tmp).value
                except:
                    LOG.debug("[%s][%s] missing" % (alltime_interval, tmp))
                    value = "0.00"
                context[tmp] = value
            # last year
            last = get_last_year(date, context['interval'])
            try:
                value = "%.2f" % Stat.objects.get(interval=context['interval'],
                                                  date=last, key=key).value
            except:
                value = "0.00"
                LOG.debug("[%s][%s][%s] missing" % (last, context['interval'],
                                                    key))
            context["last_%s" % key] = value
        context['products'] = _search_sub_key(stats, "_product_nb", Produit,
                                              True)
        context['categories'] = _search_sub_key(stats, "_category_nb",
                                                Categorie, True)
        context['vats'] = _search_sub_key(stats, "_vat", VAT)
        context['payments'] = _search_sub_key(stats, "_payment_value",
                                              PaiementType)
        context['date'] = date.isoformat()
        LOG.debug(context)
        return context
