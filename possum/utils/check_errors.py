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
"""Check errors in bills by add all products and compare with montant
"""
from decimal import Decimal
import os
import sys

from django.utils.translation import ugettext

from possum.base.models import Facture


sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'possum.settings'


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
        print("Ouch, there are errors on %d bills for %.2f%s" % (nb, diff,
                                                                 ugettext("$")))
        print("There are more money than it should.")
    else:
        print("Ouch, there are errors on %d bills for %.2f%s" % (nb, diff,
                                                                 ugettext("$")))
        print("This is very bad, there are less money than it should.")
else:
    print("Perfect, there are no errors!")
