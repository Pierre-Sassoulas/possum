#!/usr/bin/env python
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
from django.core.management.base import BaseCommand
from possum.stats.models import Stat, get_month, get_year, get_week
import datetime


def get_date(year, month, day):
    int_year = int(year)
    int_month = int(month)
    int_day = int(day)
    if int_day < 1 or int_day > 31:
        int_day = 1
    if int_month < 1 or int_day > 12:
        int_month = 1
    return datetime.date(int_year, int_month, int_day)


class Command(BaseCommand):
    args = ""
    help = "Update Stats from version 0.5 to 0.6"

    def handle(self, *args, **options):
        """7 types of interval:
        a: all time day
        b: all time month
        c: all time week
        y: year
        m: month
        w: week
        d: day
        """
        old_stats = Stat.objects.filter(date="1978-03-03")
        if old_stats.count():
            self.stdout.write("Old stats to update: %d" % old_stats.count())
            self.stdout.write("Please wait ...")
            for stat in old_stats.filter(interval="y"):
                date = get_date(stat.year, stat.month, stat.day)
                stat.date = get_year(date)
                stat.save()
            for stat in old_stats.filter(interval="m"):
                date = get_date(stat.year, stat.month, stat.day)
                stat.date = get_month(date)
                stat.save()
            for stat in old_stats.filter(interval="d"):
                stat.date = get_date(stat.year, stat.month, stat.day)
                stat.save()
            for stat in old_stats.filter(interval="w"):
                date = get_date(stat.year, 1, 1)
                if stat.week > 0:
                    date = date + datetime.timedelta(days=(stat.week - 1) * 7)
                stat.date = get_week(date)
                stat.save()
            self.stdout.write("Update 0.5 to 0.6 is done")
