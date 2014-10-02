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

from django.test import TestCase

from possum.base.models import Categorie
from possum.base.models import ProduitVendu, Produit


class Tests_Products(TestCase):
    fixtures = ['demo.json']

    def test_is_full(self):
        menu = ProduitVendu()
        menu.produit = Produit.objects.get(nom="biere 50cl")
        menu.save()
        self.assertTrue(menu.isFull())

        menu.produit = Produit.objects.get(nom="Menu Entree/Plat")
        self.assertFalse(menu.isFull())

        plat = ProduitVendu()
        plat.produit = Produit.objects.get(nom="entrecote")
        plat.save()
        menu.contient.add(plat)
        self.assertFalse(menu.isFull())

        entree = ProduitVendu()
        entree.produit = Produit.objects.get(nom="salade normande")
        entree.save()
        menu.contient.add(entree)
        self.assertTrue(menu.isFull())

    def test_free_category(self):
        menu = ProduitVendu()
        menu.produit = Produit.objects.get(nom="biere 50cl")
        menu.save()
        self.assertEqual(None, menu.getFreeCategorie())

        menu.produit = Produit.objects.get(nom="Menu Entree/Plat")
        cat_entrees = Categorie.objects.get(nom="Entrees")
        self.assertEqual(cat_entrees, menu.getFreeCategorie())

        entree = ProduitVendu()
        entree.produit = Produit.objects.get(nom="salade normande")
        entree.save()
        menu.contient.add(entree)
        cat_plats = Categorie.objects.get(nom="Plat")
        self.assertEqual(cat_plats, menu.getFreeCategorie())

        plat = ProduitVendu()
        plat.produit = Produit.objects.get(nom="entrecote")
        plat.save()
        menu.contient.add(plat)
        self.assertEqual(None, menu.getFreeCategorie())

        menu.contient.remove(entree)
        self.assertEqual(cat_entrees, menu.getFreeCategorie())

        menu.contient.add(entree)
        self.assertEqual(None, menu.getFreeCategorie())
