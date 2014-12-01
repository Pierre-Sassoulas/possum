# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('priorite', models.PositiveIntegerField(default=0)),
                ('surtaxable', models.BooleanField(
                    default=False, verbose_name=b'majoration terrasse')),
                ('disable_surtaxe', models.BooleanField(
                    default=False, verbose_name=b'peut enlever la surtaxe presente')),
                ('made_in_kitchen', models.BooleanField(default=False)),
                ('color', models.CharField(default=b'#ffdd82', max_length=8)),
            ],
            options={
                'ordering': ['priorite', 'nom'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=32)),
                ('value', models.CharField(default=b'', max_length=64)),
            ],
            options={
                'ordering': ['key'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuisson',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('nom_facture', models.CharField(default=b'', max_length=35)),
                ('priorite', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('date_creation', models.DateTimeField(
                    auto_now_add=True, verbose_name=b'creer le')),
                ('couverts', models.PositiveIntegerField(
                    default=0, verbose_name=b'nombre de couverts')),
                ('total_ttc', models.DecimalField(
                    default=0, max_digits=9, decimal_places=2)),
                ('restant_a_payer', models.DecimalField(
                    default=0, max_digits=9, decimal_places=2)),
                ('saved_in_stats', models.BooleanField(default=False)),
                ('onsite', models.BooleanField(default=True)),
                ('surcharge', models.BooleanField(default=False)),
                ('category_to_follow', models.ForeignKey(
                    blank=True, to='base.Categorie', null=True)),
            ],
            options={
                'get_latest_by': 'id',
                'permissions': (('p1', 'can use manager part'), ('p2', 'can use carte part'), ('p3', 'can use POS'), (
                    'p4', 'can ...'), ('p5', 'can ...'), ('p6', 'can ...'), ('p7', 'can ...'), ('p8', 'can ...'), ('p9', 'can ...')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(
                    auto_now_add=True, verbose_name=b'depuis le')),
                ('done', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='base.Categorie')),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'id',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(default=b'', max_length=35)),
            ],
            options={
                'ordering': ['message'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=16)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('montant', models.DecimalField(
                    default=0, max_digits=9, decimal_places=2)),
                ('valeur_unitaire', models.DecimalField(
                    default=1, max_digits=9, decimal_places=2)),
                ('date', models.DateTimeField(
                    auto_now_add=True, verbose_name=b'encaisser le')),
                ('nb_tickets', models.PositiveIntegerField(default=0)),
            ],
            options={
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaiementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('fixed_value', models.BooleanField(
                    default=False, verbose_name=b'ticket ?')),
            ],
            options={
                'ordering': ['nom'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('options', models.CharField(max_length=120)),
                ('header', models.TextField(default=b'')),
                ('footer', models.TextField(default=b'')),
                ('width', models.PositiveIntegerField(default=27)),
                ('kitchen_lines', models.IntegerField(default=0)),
                ('kitchen', models.BooleanField(default=False)),
                ('billing', models.BooleanField(default=False)),
                ('manager', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('choix_cuisson', models.BooleanField(default=False)),
                ('actif', models.BooleanField(default=True)),
                ('prix', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('price_surcharged', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('vat_onsite', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('vat_surcharged', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('vat_takeaway', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('categorie', models.ForeignKey(
                    related_name='produit-categorie', to='base.Categorie')),
                ('categories_ok', models.ManyToManyField(to='base.Categorie')),
                ('options_ok', models.ManyToManyField(
                    to='base.Option', null=True, blank=True)),
                ('produits_ok', models.ManyToManyField(
                    related_name='produits_ok_rel_+', to='base.Produit')),
            ],
            options={
                'ordering': ['categorie', 'nom'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProduitVendu',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('prix', models.DecimalField(
                    default=0, max_digits=7, decimal_places=2)),
                ('sent', models.BooleanField(default=False)),
                ('contient', models.ManyToManyField(
                    related_name='contient_rel_+', to='base.ProduitVendu')),
                ('cuisson', models.ForeignKey(
                    related_name='produitvendu-cuisson', blank=True, to='base.Cuisson', null=True)),
                ('made_with', models.ForeignKey(
                    related_name='produit-kitchen', to='base.Categorie', null=True)),
                ('notes', models.ManyToManyField(
                    to='base.Note', null=True, blank=True)),
                ('options', models.ManyToManyField(
                    to='base.Option', null=True, blank=True)),
                ('produit', models.ForeignKey(
                    related_name='produitvendu-produit', to='base.Produit')),
            ],
            options={
                'ordering': ['produit'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VAT',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('tax', models.DecimalField(
                    default=0, max_digits=4, decimal_places=2)),
                ('value', models.DecimalField(
                    default=0, max_digits=6, decimal_places=4)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VATOnBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(
                    default=0, max_digits=9, decimal_places=2)),
                ('vat', models.ForeignKey(
                    related_name='bill-vat', to='base.VAT')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                 serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('surtaxe', models.BooleanField(
                    default=False, verbose_name=b'zone surtax\xc3\xa9e ?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='table',
            name='zone',
            field=models.ForeignKey(related_name='table-zone', to='base.Zone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paiement',
            name='type',
            field=models.ForeignKey(
                related_name='paiement-type',
                to='base.PaiementType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follow',
            name='produits',
            field=models.ManyToManyField(
                related_name='les produits envoyes',
                to='base.ProduitVendu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='following',
            field=models.ManyToManyField(
                to='base.Follow',
                null=True,
                blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='in_use_by',
            field=models.ForeignKey(
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='paiements',
            field=models.ManyToManyField(
                related_name='les paiements',
                to='base.Paiement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='produits',
            field=models.ManyToManyField(
                related_name='les produits vendus',
                to='base.ProduitVendu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='table',
            field=models.ForeignKey(
                related_name='facture-table',
                blank=True,
                to='base.Table',
                null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facture',
            name='vats',
            field=models.ManyToManyField(
                related_name='vat total for each vat on a bill',
                to='base.VATOnBill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categorie',
            name='vat_onsite',
            field=models.ForeignKey(
                related_name='categorie-vat-onsite',
                blank=True,
                to='base.VAT',
                null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categorie',
            name='vat_takeaway',
            field=models.ForeignKey(
                related_name='categorie-vat-takeaway',
                blank=True,
                to='base.VAT',
                null=True),
            preserve_default=True,
        ),
    ]
