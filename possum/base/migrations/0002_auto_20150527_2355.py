# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ['nom']},
        ),
        migrations.AlterModelOptions(
            name='zone',
            options={'ordering': ['nom']},
        ),
    ]
