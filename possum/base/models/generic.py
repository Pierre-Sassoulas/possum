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


class Nom(models.Model):
    nom = models.CharField(max_length=60)

    def __str__(self):
        return self.nom

    class Meta:
        abstract = True
        ordering = ['nom']


class NomDouble(Nom):
    nom_facture = models.CharField(max_length=35, default="")

    class Meta:
        abstract = True


class Priorite(models.Model):

    """Getter / setter: si priorite inferieur à 0 on reste à 0
    """
    priorite = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['priorite']

    def set_less_priority(self, number=1):
        ''' Set a lower priority
        :param int number:
        '''
        tmp = self.priorite - number
        if tmp < 0:
            self.priorite = 0
        else:
            self.priorite = tmp
        self.save()

    def set_more_priority(self, number=1):
        ''' Set a higher priority
        :param int number:
        '''
        self.priorite += number
        self.save()
