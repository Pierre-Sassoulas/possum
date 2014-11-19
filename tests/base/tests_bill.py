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

from decimal import Decimal

from django.test import TestCase

from possum.base.models import Facture, PaiementType, Paiement, ProduitVendu, \
    Produit


class TestsBill(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        TestCase.setUp(self)
        self.facture = Facture()
        self.facture.save()
        self.plat = ProduitVendu()
        self.plat.produit = Produit.objects.get(nom="entrecote")

    def test_is_empty(self):
        self.assertTrue(self.facture.is_empty())
        self.facture.add_product(self.plat)
        self.assertFalse(self.facture.is_empty())

    def test_add_product(self):
        self.assertTrue(self.facture.is_empty())
        self.facture.add_product(self.plat)
        self.facture.update()
        self.assertTrue(self.plat in self.facture.produits.iterator())
        self.assertEqual(self.plat.produit.prix, self.facture.total_ttc)
        self.assertEqual(self.plat.produit.prix, self.facture.restant_a_payer)

    def test_del_payment(self):
        payment = Paiement()
        montant = 42
        valeur_unitaire = 73
        paymentType = PaiementType()
        payment.montant = 73
        payment.type = paymentType
        payment.valeur_unitaire = Decimal(valeur_unitaire)
        payment.montant = Decimal(montant)
        self.facture.add_payment(paymentType, montant, valeur_unitaire)
        self.facture.del_payment(payment)

    def test_is_valid_payment(self):
        self.assertFalse(self.facture.is_valid_payment(42))
        self.facture.add_product(self.plat)
        self.facture.update()
        self.assertTrue(self.facture.is_valid_payment(42))
        self.facture.restant_a_payer = Decimal("0")
        self.assertFalse(self.facture.is_valid_payment(42))

    def test_rendre_monnaie(self):
        payment = Paiement()
        payment.type = PaiementType()
        payment.montant = Decimal("900")
        self.facture.add_product(self.plat)
        self.facture.update()
        self.facture.rendre_monnaie(payment)
        left = self.facture.total_ttc - Decimal("900")
        self.assertEqual(left, self.facture.paiements.all()[0].montant)

    def test_add_payment(self):
        self.facture.add_product(self.plat)
        self.facture.update()
        self.facture.add_payment(PaiementType.objects.get(nom="CB"), "2")
        restant_a_payer = Decimal(str(self.plat.produit.prix - 2))
        self.assertEqual(self.facture.restant_a_payer, restant_a_payer)
        self.facture.add_payment(PaiementType.objects.get(nom="Espece"), "10")
        self.assertEqual(self.facture.restant_a_payer, Decimal(0))
        montant = Decimal(str(self.plat.produit.prix - 12))
        self.assertEqual(montant, (self.facture.paiements.all()[2]).montant)
        # TODO This is done just to execute more code
        # An assertion should be verified
        self.facture.print_ticket_kitchen()
        self.facture.est_un_repas()
        self.facture.print_ticket()
