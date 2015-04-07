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

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from possum.base.models import (Categorie, Cuisson, Paiement, PaiementType,
                                Facture, Produit, Follow, Table, Zone, VAT,
                                Printer, VATOnBill, Config)
from possum.stats.models import Stat


class Command(BaseCommand):
    args = ""
    help = "Initialize database"

    def handle(self, *args, **options):
        self.stdout.write("Erase objects in database")
        VAT.objects.all().delete()
        Printer.objects.all().delete()
        VATOnBill.objects.all().delete()
        Categorie.objects.all().delete()
        Produit.objects.all().delete()
        Stat.objects.all().delete()
        Follow.objects.all().delete()
        Facture.objects.all().delete()
        Zone.objects.all().delete()
        Table.objects.all().delete()
        User.objects.all().delete()
        PaiementType.objects.all().delete()
        Paiement.objects.all().delete()
        Config.objects.all().delete()

        Cuisson(priorite=10, nom_facture="B", nom="bleu").save()
        Cuisson(priorite=15, nom_facture="S", nom="saignant").save()
        Cuisson(priorite=20, nom_facture="AP", nom="a point").save()
        Cuisson(priorite=25, nom_facture="BC", nom="bien cuit").save()

        self.stdout.write("Add a manager")
        user = User(username="demo",
                    first_name="first name",
                    last_name="last name",
                    email="demo@possum-software.org")
        user.set_password("demo")
        self.stdout.write("Setup permissions for manager")
        user.is_superuser = True
        user.save()

        self.stdout.write("Add a pos user")
        user = User(username="pos", first_name="", last_name="", email="")
        user.set_password("pos")
        user.save()

        self.stdout.write("Setup type of payments")
        PaiementType(nom='AMEX', fixed_value=False).save()
        PaiementType(nom='ANCV', fixed_value=True).save()
        PaiementType(nom='CB', fixed_value=False).save()
        PaiementType(nom='Cheque', fixed_value=False).save()
        PaiementType(nom='Espece', fixed_value=False).save()
        PaiementType(nom='Tic. Resto.', fixed_value=True).save()

        # Type de paiements par défaut pour les remboursements lorsque
        # le paiement dépasse le montant de la facture
        id_type_paiement = PaiementType.objects.get(nom="Espece").id
        Config(key="payment_for_refunds", value=id_type_paiement).save()

        # Default PaymentType to select by default on the payment page
        # Comment out this 2 lines if you want it
        # id_type_paiement = PaiementType.objects.get(nom="Espece").id
        # Config(key="default_type_payment", value=id_type_paiement).save()

        # Le montant de surtaxe, si utilisé
        Config(key="price_surcharge", value="0.20").save()
