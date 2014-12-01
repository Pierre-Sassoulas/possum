# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.CharField(default=b'd', max_length=1, choices=[(b'a', b'All time day'), (b'b', b'All time month'), (
                    b'c', b'All time week'), (b'y', b'Year'), (b'w', b'Week'), (b'm', b'Month'), (b'd', b'Day')])),
                ('year', models.PositiveIntegerField(default=0)),
                ('month', models.PositiveIntegerField(default=0)),
                ('day', models.PositiveIntegerField(default=0)),
                ('week', models.PositiveIntegerField(default=0)),
                ('key', models.CharField(max_length=32)),
                ('value', models.DecimalField(
                    default=0, max_digits=9, decimal_places=2)),
            ],
            options={
                'ordering': ['interval', 'year', 'month', 'day', 'key'],
            },
            bases=(models.Model,),
        ),
    ]
