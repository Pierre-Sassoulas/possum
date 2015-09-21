# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facture',
            options={'get_latest_by': 'id'},
        ),
        migrations.RemoveField(
            model_name='produitvendu',
            name='cuisson',
        ),
        migrations.AddField(
            model_name='produitvendu',
            name='cooking',
            field=models.SmallIntegerField(default=1, choices=[(0, b'Bleu'), (1, b'Saignant'), (2, b'A point'), (3, b'Bien cuit')]),
        ),
        migrations.DeleteModel(
            name='Cuisson',
        ),
    ]
