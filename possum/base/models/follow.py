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

from django.db import models

from possum.base.models.category import Categorie
from possum.base.models.product_sold import ProduitVendu


class Follow(models.Model):

    """Suivi des envois en cuisine:
    category est la categorie envoyée en cuisine"""
    category = models.ForeignKey(Categorie)
    date = models.DateTimeField('depuis le', auto_now_add=True)
    produits = models.ManyToManyField(ProduitVendu,
                                      related_name="sent_product")
    done = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'id'
        ordering = ['date']

    def time(self):
        return self.date.strftime("%H:%M")

    def __unicode__(self):
        return "[%s] %s" % (self.date.strftime("%H:%M"), self.category.nom)
