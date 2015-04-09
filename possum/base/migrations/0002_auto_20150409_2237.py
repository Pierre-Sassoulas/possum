# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='following',
            field=models.ManyToManyField(to='base.Follow', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produit',
            name='options_ok',
            field=models.ManyToManyField(to='base.Option', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='notes',
            field=models.ManyToManyField(to='base.Note', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='options',
            field=models.ManyToManyField(to='base.Option', blank=True),
            preserve_default=True,
        ),
    ]
