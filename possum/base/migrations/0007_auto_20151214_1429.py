# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20150715_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='color',
            field=models.CharField(max_length=8, default='#ffdd82'),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='disable_surtaxe',
            field=models.BooleanField(default=False, verbose_name='peut enlever la surtaxe presente'),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='surtaxable',
            field=models.BooleanField(default=False, verbose_name='majoration terrasse'),
        ),
        migrations.AlterField(
            model_name='config',
            name='value',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AlterField(
            model_name='facture',
            name='couverts',
            field=models.PositiveIntegerField(verbose_name='nombre de couverts', default=0),
        ),
        migrations.AlterField(
            model_name='facture',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creer le'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='depuis le'),
        ),
        migrations.AlterField(
            model_name='note',
            name='message',
            field=models.CharField(max_length=35, default=''),
        ),
        migrations.AlterField(
            model_name='option',
            name='name',
            field=models.CharField(max_length=16, default=''),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='cashed on'),
        ),
        migrations.AlterField(
            model_name='paiementtype',
            name='fixed_value',
            field=models.BooleanField(default=False, verbose_name='ticket ?'),
        ),
        migrations.AlterField(
            model_name='printer',
            name='footer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='printer',
            name='header',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='cooking',
            field=models.SmallIntegerField(default=42, choices=[(0, 'Bleu'), (1, 'Saignant'), (2, 'A point'), (3, 'Bien cuit')]),
        ),
        migrations.AlterField(
            model_name='zone',
            name='surtaxe',
            field=models.BooleanField(default=False, verbose_name='zone surtaxée ?'),
        ),
    ]
