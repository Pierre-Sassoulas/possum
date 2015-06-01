#!/usr/bin/env python
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
from django.core.management.base import BaseCommand
from possum.stats.models import Stat
from possum.base.models import Facture
import datetime


class Command(BaseCommand):
    args = "<year ...>"
    help = "Update statistics"

    def handle(self, *args, **options):
        for year in args:
            before = datetime.datetime.now()
            self.stdout.write("[%s] delete stats before update" %
                              datetime.datetime.now().strftime("%H:%M"))
            Stat.objects.filter(year=year).delete()

            self.stdout.write(
                "[%s] change status for bills" %
                datetime.datetime.now().strftime("%H:%M"))
            begin = "%d-01-01 00:00:00" % year
            end = "%d-12-31 23:59:59" % year
            bills = Facture.objects.filter(date_creation__gte=begin,
                                           date_creation__lt=end)
            for bill in bills.iterator():
                bill.saved_in_stats = False
                bill.save()

            self.stdout.write("[%s] compute stats" %
                              datetime.datetime.now().strftime("%H:%M"))
            Stat().update()

            after = datetime.datetime.now()
            diff = after - before
            time = ""
            if diff.seconds > 3600:
                # more than a hour
                hour = diff.seconds / 3600
                mn = (diff.seconds % 3600) / 60
                time = "%dh %dm" % (hour, mn)
            else:
                mn = diff.seconds / 60
                sec = diff.seconds % 60
                time = "%dm %ds" % (mn, sec)
            self.stdout.write("[%d] updated %d bills in %s" % (year,
                              bills.count(), time))
