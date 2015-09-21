# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_stat_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stat',
            options={'ordering': ['interval', 'date', 'key']},
        ),
    ]
