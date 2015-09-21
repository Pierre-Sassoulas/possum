# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20150715_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produitvendu',
            name='cooking',
            field=models.SmallIntegerField(default=42, choices=[(0, b'Bleu'), (1, b'Saignant'), (2, b'A point'), (3, b'Bien cuit')]),
        ),
    ]
