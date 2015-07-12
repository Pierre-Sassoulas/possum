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
from datetime import datetime
import logging

from django.db import models


LOG = logging.getLogger(__name__)


class Config(models.Model):

    """Possum Configuration
    """
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=64, default="")

    def __unicode__(self):
        return self.key

    def __cmp__(self, other):
        '''
        :param Config other: A config to be compared to this one.
        :return: Boolean
        '''
        return cmp(self.key, other.key)

    class Meta:
        ordering = ['key']

    def carte_changed(self, date):
        ''' Check if carte has changed since 'date'

        True: carte has changed
        False: no change

        :param date: str with last modification for this carte.
        :return etype: Boolean
        '''
        LOG.debug("will test this date: [%s]" % date)
        record = self.get_carte_changed()
        if date == record.value:
            LOG.debug("[last_carte_changed] no change")
            return False
        else:
            LOG.debug("[last_carte_changed] has changed")
            return True

    def set_carte_changed(self):
        """Record now has last changed date for carte
        :return: Config()
        """
        LOG.debug("[last_carte_changed] set new date")
        record = self.get_carte_changed()
        record.value = datetime.now().strftime("%Y%m%d-%H%M")
        record.save()
        return record

    def get_carte_changed(self):
        """
        :return: Config for last date carte has changed
        """
        try:
            record = Config.objects.get(key="last_carte_changed")
        except Config.DoesNotExist:
            LOG.debug("[last_carte_changed] created")
            record = Config(key="last_carte_changed")
            record.value = datetime.now().strftime("%Y%m%d-%H%M")
            record.save()
        return record
