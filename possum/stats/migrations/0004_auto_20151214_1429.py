# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20150209_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='date',
            field=models.DateField(default='1978-03-03'),
        ),
        migrations.AlterField(
            model_name='stat',
            name='interval',
            field=models.CharField(choices=[('a', 'All time day'), ('b', 'All time month'), ('c', 'All time week'), ('y', 'Year'), ('w', 'Week'), ('m', 'Month'), ('d', 'Day')], default='d', max_length=1),
        ),
    ]
