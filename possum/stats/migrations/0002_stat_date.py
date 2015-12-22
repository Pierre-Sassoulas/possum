# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='date',
            field=models.DateField(default='1978-03-03'),
            preserve_default=True,
        ),
    ]
