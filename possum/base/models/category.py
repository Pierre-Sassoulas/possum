# -*- coding: utf-8 -*-
#
#    Copyright 2009-2014 Sébastien Bonnegent
#
#    This file is part of POSSUM.
#
#    POSSUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published
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

from possum.base.models.config import Config
from possum.base.models.generic import Nom, Priorite
from possum.base.models.vat import VAT


class Categorie(Nom, Priorite):

    """Category of products

    :param Boolean surtaxable: there are a surtaxe on this category
    :param Boolean disable_surtaxe:
    :param Boolean made_in_kitchen: must be cooked in kitchen
    :param String color:
    :param VAT vat_onsite:
    :param VAT vat_takeaway:
    """
    surtaxable = models.BooleanField("majoration terrasse", default=False)
    disable_surtaxe = models.BooleanField("peut enlever la surtaxe presente",
                                          default=False)
    made_in_kitchen = models.BooleanField(default=False)
    color = models.CharField(max_length=8, default="#ffdd82")
    vat_onsite = models.ForeignKey(VAT, null=True, blank=True,
                                   related_name="categorie_vat_onsite")
    vat_takeaway = models.ForeignKey(VAT, null=True, blank=True,
                                     related_name="categorie_vat_takeaway")

    def __cmp__(self, other):
        ''' Classement par priorite_facture (plus la valeur est petite,
        plus elle est prioritaire), puis par nom_ihm en cas d'égalité.

        :param other:
        :type other:
        '''
        if self.priorite == other.priorite:
            return cmp(self.nom, other.nom)
        else:
            return cmp(self.priorite, other.priorite)

    def set_vat_takeaway(self, vat):
        '''
        TODO
        :param vat:
        :type vat:
        '''
        self.vat_takeaway = vat
        self.save()
        # il faut toujours faire un product.update_vats()

    def set_vat_onsite(self, vat):
        '''
        TODO
        :param vat:
        :type vat:
        '''
        self.vat_onsite = vat
        self.save()

    def save(self, force_insert=False, using=None):
        ''' We overload this method to keep last date carte has changed

        :param Boolean force_insert:
        :param using: TODO
        :type using:
        '''
        Config().set_carte_changed()
        super(Categorie, self).save(force_insert=force_insert, using=using)

    class Meta:
        app_label = 'base'
        ordering = ['priorite', 'nom']
