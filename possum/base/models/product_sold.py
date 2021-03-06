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

import logging

from django.db import models
from django.utils.translation import ugettext as _

from possum.base.models.category import Categorie
from possum.base.models.note import Note
from possum.base.models.options import Option
from possum.base.models.product import Produit


LOG = logging.getLogger(__name__)


class ProduitVendu(models.Model):
    """le prix sert a affiche correctement les prix pour les surtaxes

    :param options: options sélectionnées
    :param cooking: cuissons
    """
    TYPE_COOKING = ((0, "Bleu"), (1, "Saignant"), (2, "A point"),
                    (3, "Bien cuit"))
    SHORT = ["B", "S", "AP", "BC"]
    date = models.DateTimeField(auto_now_add=True)
    produit = models.ForeignKey(Produit, related_name="produit_vendu_produit")
    cooking = models.SmallIntegerField(choices=TYPE_COOKING, default=42)
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    options = models.ManyToManyField(Option, blank=True)
    # dans le cas d'un menu, peut contenir d'autres produits
    contient = models.ManyToManyField('self')
    notes = models.ManyToManyField(Note, blank=True)
    # faut-il préparer ce plat avec les entrées ?
    made_with = models.ForeignKey(Categorie, related_name="produit_kitchen",
                                  null=True)
    # a-t-il été envoyé en cuisine
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['produit', ]

    def __str__(self):
        """ Different display if we have a menu or not
        """
        if self.notes.count():
            tmp = "* "
        else:
            tmp = ""
        tmp += self.produit.nom
        if self.prix:
            tmp += " (%.2f)" % self.prix
        if self.produit.categories_ok.count():
            # cas du menu
            products = []
            for sold in self.contient.iterator():
                name = sold.produit.nom[:6]
                name += sold.get_cooking()
                products.append(name)
            tmp += " "
            tmp += "/".join(products)
        else:
            # cas d'un Produit simple
            tmp += " %s" % self.get_cooking()
        return tmp

    def __lt__(self, other):
        if self.produit.categorie == other.produit.categorie:
            return (self.produit.nom < other.produit.nom)
        else:
            return (self.produit.categorie < other.produit.categorie)

    def is_cooking_set(self):
        """
        :return: Boolean
        """
        if self.produit.choix_cuisson and self.cooking == 42:
            return False
        return True

    def get_cooking(self, short=False):
        """Give product cooking
        If short, we give only one or two letter.

        :param short: Boolean"""
        if self.produit.choix_cuisson:
            if short:
                try:
                    return _(self.SHORT[self.cooking])
                except:
                    return "ND"
            else:
                try:
                    return _(self.TYPE_COOKING[self.cooking][1])
                except:
                    return "Not Defined"
        else:
            return ""

    def set_cooking(self, cooking):
        """Set cooking level
        :param cooking: int cooking id
        """
        try:
            new = int(cooking)
        except:
            LOG.warning("bad cooking id")
            return False
        if new > -1 and new < len(self.SHORT):
            LOG.info("[%s] cooking = %d" % (self.id, new))
            self.cooking = new
            self.save()
            return True
        else:
            LOG.warning("[%s] invalid cooking %d" % (self.id, new))
            return False

    def is_full(self):
        """
        True if all the elements  (sub products for a formule) are presents
        else false.
        :return: Boolean
        """
        nb_produits = self.contient.count()
        nb_categories = self.produit.categories_ok.count()
        if nb_produits == nb_categories:
            LOG.debug("product is full")
            return True
        elif nb_produits > nb_categories:
            msg = "product id [%s] have more products" % self.id
            msg += " that categories authorized"
            LOG.warning(msg)
            return True
        else:
            LOG.debug("product is not full")
            return False

    def est_un_menu(self):
        '''
        On a un menu si on a plus d'un produit.
        :return: boolean
        '''
        return self.produit.categories_ok.count()

    def get_free_categorie(self):
        """

        :return: La premiere categorie dans la liste categories_ok qui n'a pas\
        de produit dans la partir 'contient'. Sinon retourne None.
        """
        if self.produit.categories_ok.count() > 0:
            for categorie in self.produit.categories_ok.order_by("priorite"):
                if self.contient.filter(
                        produit__categorie=categorie).count() == 0:
                    return categorie
        else:
            msg = "Product [%s] have no categories_ok, return None" % self.id
            LOG.warning(msg)
        return None

    def get_identifier(self):
        """
        :return: un identifiant qui défini le Produit() et ses options
        """
        if self.notes.count():
            notes = "N".join([str(i.id) for i in self.notes.all()])
        else:
            notes = ""
        if self.options.count():
            options = "O".join([str(i.id) for i in self.options.all()])
        else:
            options = ""
        if self.produit:
            produit = str(self.produit.id)
        else:
            produit = ""
        return "P%s_C%s_O%s_N%s" % (produit, self.cooking, options, notes)

    def set_prize(self, prize):
        ''' Set prize for the product sold
        :param Decimal prize:
        '''
        if self.prix != prize:
            LOG.debug("[%s] prize: %s > %s" % (self.id, self.prix, prize))
            self.prix = prize
            self.save()
