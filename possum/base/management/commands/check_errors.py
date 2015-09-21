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
from decimal import Decimal
from django.utils.translation import ugettext as _
from possum.base.models import Facture


class Command(BaseCommand):
    args = ""
    help = "Check errors in bills by adding all products and compare with "\
           "montant"

    def handle(self, *args, **options):
        self.stdout.write("Compute...")

        diff = Decimal("0")
        nb = 0

        for bill in Facture.objects.all():
            montant = Decimal("0")
            for sold in bill.produits.all():
                if bill.surcharge:
                    montant += sold.produit.price_surcharged
                else:
                    montant += sold.produit.prix
            if montant != bill.total_ttc:
                nb += 1
                diff += bill.total_ttc - montant

        if nb:
            if diff > Decimal("0"):
                self.stdout.write("Ouch, there are errors on %d bills for "
                                  "%.2f%s" % (nb, diff, _("$")))
                self.stdout.write("There are more money than it should.")
            else:
                self.stdout.write("Ouch, there are errors on %d bills for "
                                  "%.2f%s" % (nb, diff, _("$")))
                self.stdout.write("This is very bad, there are less money than"
                                  "it should.")
        else:
            self.stdout.write("Perfect, there are no errors!")
