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


class TestsCategories(TestCase):

    def test_cmp(self):
        cat1 = Categorie(nom="nom1", priorite=1)
        cat2 = Categorie(nom="nom2")
        cat3 = Categorie(nom="nom3", priorite=1)
        liste = []
        liste.append(cat3)
        liste.append(cat2)
        liste.append(cat1)
        self.assertEqual([cat3, cat2, cat1], liste)
        liste.sort()
        self.assertEqual([cat2, cat1, cat3], liste)
