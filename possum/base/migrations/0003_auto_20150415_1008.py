# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150415_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='options_ok',
            field=models.ManyToManyField(to='base.Option', blank=True),
        ),
    ]
