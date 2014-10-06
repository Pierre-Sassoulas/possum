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

import datetime

from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stat'
        db.create_table(u'stats_stat', (
            (u'id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('interval', self.gf('django.db.models.fields.CharField')
             (default='d', max_length=1)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')
             (default=0)),
            ('month', self.gf('django.db.models.fields.PositiveIntegerField')
             (default=0)),
            ('day', self.gf('django.db.models.fields.PositiveIntegerField')
             (default=0)),
            ('week', self.gf('django.db.models.fields.PositiveIntegerField')
             (default=0)),
            ('key', self.gf('django.db.models.fields.CharField')
             (max_length=32)),
            ('value', self.gf('django.db.models.fields.DecimalField')
             (default=0, max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal(u'stats', ['Stat'])

    def backwards(self, orm):
        # Deleting model 'Stat'
        db.delete_table(u'stats_stat')

    models = {
        u'stats.stat': {
            'Meta': {
                'ordering': "['year', 'month', 'day', 'key']",
                'object_name': 'Stat'},
            'day': (
                'django.db.models.fields.PositiveIntegerField',
                [],
                {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': (
                'django.db.models.fields.CharField',
                [],
                {'default': "'d'",
                 'max_length': '1'}),
            'key': (
                'django.db.models.fields.CharField',
                [],
                {'max_length': '32'}),
            'month': (
                'django.db.models.fields.PositiveIntegerField',
                [],
                {'default': '0'}),
            'value': (
                'django.db.models.fields.DecimalField',
                [],
                {'default': '0',
                 'max_digits': '9',
                 'decimal_places': '2'}),
            'week': (
                'django.db.models.fields.PositiveIntegerField',
                [],
                {'default': '0'}),
            'year': (
                'django.db.models.fields.PositiveIntegerField',
                [],
                {'default': '0'})
        }
    }

    complete_apps = ['stats']
