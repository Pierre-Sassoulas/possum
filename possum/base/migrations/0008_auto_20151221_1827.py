# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20151214_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facture',
            options={'get_latest_by': 'id', 'ordering': ['date_creation', 'table']},
        ),
    ]
