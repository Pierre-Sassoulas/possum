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

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import datetime
import random

from possum.base.models import (Categorie, Zone, VAT, Config, Table, Facture,
                                PaiementType, Produit, ProduitVendu, Option,
                                Note)
from possum.stats.models import Stat


def create_users():
    # managers
    for username in ['demo', 'demo1', 'demo2']:
        user = User(username=username, first_name=username,
                    email="%s@possum-software.org" % username)
        user.set_password(username)
        user.is_superuser = True
        user.save()

    # staff members
    for username in ['staff', 'staff1', 'staff2']:
        user = User(username=username, first_name=username,
                    email="%s@possum-software.org" % username)
        user.set_password(username)
        user.save()

def create_payment():
    # Type de paiements
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
    id_type_paiement = PaiementType.objects.get(nom="Espece").id
    Config(key="default_type_payment", value=id_type_paiement).save()

def create_tables():
    # Tables
    z = Zone(nom='Bar', surtaxe=False)
    z.save()
    Table(nom="T--", zone=z).save()
    z = Zone(nom='Rez de chaussee', surtaxe=False)
    z.save()
    for i in xrange(1, 15):
        Table(nom="T%02d" % i, zone=z).save()
    z = Zone(nom='Terrasse', surtaxe=True)
    z.save()
    for i in xrange(15, 26):
        Table(nom="T%02d" % i, zone=z).save()


class Command(BaseCommand):
    args = ""
    help = "Initialize a demo database"

    def handle(self, *args, **options):
        create_users()
        create_payment()

        # Montant de la surtaxe
        Config(key="price_surcharge", value="0.20").save()

        create_tables()

        # TVA
        vat_alcool = VAT(name="alcool")
        vat_alcool.set_tax("20")
        vat_alcool.save()
        vat_onsite = VAT(name="sur place")
        vat_onsite.set_tax("10")
        vat_onsite.save()
        vat_takeaway = VAT(name=u"à emporter")
        vat_takeaway.set_tax("7")
        vat_takeaway.save()

        # Options
        Option(name="A_Frites").save()
        Option(name="A_Salade").save()
        Option(name="S_Creme").save()
        Option(name="A_Haricots").save()
        Option(name="S_Mayo").save()

        # Notes
        Note(message="Pas de sel").save()
        Note(message="Sans champignon").save()

        #
        # Data example

        # on entre les nouveaux produits, les prix sont TTC
        jus = Categorie(nom="Jus",
                        priorite=25,
                        surtaxable=False,
                        disable_surtaxe=False,
                        made_in_kitchen=False,
                        color="#44b3dc",
                        vat_onsite=vat_onsite,
                        vat_takeaway=vat_takeaway)
        jus.save()
        abricot = Produit(nom="jus abricot",
                          prix="2.80",
                          choix_cuisson=False,
                          categorie=jus)
        abricot.save()
        pomme = Produit(nom="jus pomme",
                        prix="2.80",
                        choix_cuisson=False,
                        categorie=jus)
        pomme.save()

        bieres = Categorie(nom="Bieres",
                           priorite=2,
                           surtaxable=False,
                           disable_surtaxe=False,
                           made_in_kitchen=False,
                           color="#ea97b5",
                           vat_onsite=vat_alcool,
                           vat_takeaway=vat_alcool)
        bieres.save()
        biere = Produit(nom="biere 50cl",
                        prix="2.80",
                        choix_cuisson=False,
                        categorie=bieres)
        biere.save()

        entrees = Categorie(nom="Entrees",
                            priorite=5,
                            surtaxable=False,
                            disable_surtaxe=False,
                            made_in_kitchen=True,
                            color="#ff9f00",
                            vat_onsite=vat_onsite,
                            vat_takeaway=vat_takeaway)
        entrees.save()
        salade = Produit(nom="salade normande",
                         prix="3.40",
                         choix_cuisson=False,
                         categorie=entrees)
        salade.save()
        buffet = Produit(nom="buffet",
                         prix="6.40",
                         choix_cuisson=False,
                         categorie=entrees)
        buffet.save()

        plat = Categorie(nom="Plat",
                         priorite=10,
                         surtaxable=False,
                         disable_surtaxe=False,
                         made_in_kitchen=True,
                         color="#c9a100",
                         vat_onsite=vat_onsite,
                         vat_takeaway=vat_takeaway)
        plat.save()
        entrecote = Produit(nom="entrecote",
                            prix="8.40",
                            choix_cuisson=True,
                            categorie=plat)
        entrecote.save()
        pave = Produit(nom="pave de saumon",
                       prix="9.40",
                       choix_cuisson=False,
                       categorie=plat)
        pave.save()

        # pour les menu
        menu = Categorie(nom="Menu",
                         priorite=22,
                         surtaxable=False,
                         disable_surtaxe=False,
                         made_in_kitchen=False,
                         color="#88f027",
                         vat_onsite=vat_onsite,
                         vat_takeaway=vat_takeaway)
        menu.save()
        entree_plat = Produit(nom=u"Menu Entree/Plat",
                              prix="13.40",
                              choix_cuisson=False,
                              categorie=menu)
        entree_plat.save()
        entree_plat.categories_ok.add(entrees)
        entree_plat.categories_ok.add(plat)
        entree_plat.produits_ok.add(salade)
        entree_plat.produits_ok.add(entrecote)
        entree_plat.produits_ok.add(pave)
        entree_plat.save()

        # mis a jour des TTC et TVA
        for product in Produit.objects.all():
            product.update_vats(keep_clone=False)

        def create_bill(finish=True):
            """Create a bill
            """
            table = 'T%d' % random.randint(10, 25)
            bill = Facture(table=Table.objects.get(nom=table))
            bill.save()
            produits_bar = [biere, pomme, abricot]
            produits_guests = [salade, buffet, entrecote, pave]
            payments = ['CB', 'Espece', 'Cheque']
            if random.randint(1, 2) == 1:
                # guests part
                produits = produits_guests
                bill.couverts = random.randint(1, 15)
            else:
                produits = produits_bar
            nb_produits = random.randint(1, 6)
            for i in xrange(nb_produits):
                # random number of products
                nb_max = len(produits) - 1
                produit = produits[random.randint(0, nb_max)]
                sold = ProduitVendu(produit=produit)
                sold.save()
                bill.add_product(sold)
            # nouveau_menu = ProduitVendu(produit=entree_plat)
            # nouveau_menu.save()
            # for produit in [salade, pave]:
                # sold = ProduitVendu(produit=produit)
                # sold.save()
                # nouveau_menu.contient.add(sold)
            # nouveau_menu.save()
            bill.update()
            if finish:
                nb_max = len(payments) - 1
                name = payments[random.randint(0, nb_max)]
                type_payment = PaiementType.objects.get(nom=name)
                bill.add_payment(type_payment, bill.total_ttc)
            return bill

        # on ajoute des données pour avoir des jolies graphiques de
        # démonstrations
        now = datetime.datetime.now()
        for month in xrange(1, 13):
            for i in xrange(20):
                day = random.randint(1, 28)
                bill = create_bill()
                bill.date_creation = datetime.datetime(now.year, month, day)
                bill.save()

        # Création d'une dizaine de facture
        for i in xrange(15):
            bill = create_bill(finish=False)
            if i % 2:
                bill.update_kitchen()
                bill.print_ticket_kitchen()

        Stat().update()
