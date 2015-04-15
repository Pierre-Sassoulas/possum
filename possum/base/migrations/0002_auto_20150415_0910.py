# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='vat_onsite',
            field=models.ForeignKey(related_name='categorie_vat_onsite', blank=True, to='base.VAT', null=True),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='vat_takeaway',
            field=models.ForeignKey(related_name='categorie_vat_takeaway', blank=True, to='base.VAT', null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='following',
            field=models.ManyToManyField(to='base.Follow', blank=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='paiements',
            field=models.ManyToManyField(related_name='payments', to='base.Paiement'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='produits',
            field=models.ManyToManyField(related_name='sold_product', to='base.ProduitVendu'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='table',
            field=models.ForeignKey(related_name='table_bill', blank=True, to='base.Table', null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='vats',
            field=models.ManyToManyField(related_name='total_vat', to='base.VATOnBill'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='produits',
            field=models.ManyToManyField(related_name='sent_product', to='base.ProduitVendu'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'cashed on'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='type',
            field=models.ForeignKey(related_name='payment_type', to='base.PaiementType'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(related_name='product_category', to='base.Categorie'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='options_ok',
            field=models.ManyToManyField(to='base.Option'),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='cuisson',
            field=models.ForeignKey(related_name='produit_vendu_cuisson', blank=True, to='base.Cuisson', null=True),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='made_with',
            field=models.ForeignKey(related_name='produit_kitchen', to='base.Categorie', null=True),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='notes',
            field=models.ManyToManyField(to='base.Note', blank=True),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='options',
            field=models.ManyToManyField(to='base.Option', blank=True),
        ),
        migrations.AlterField(
            model_name='produitvendu',
            name='produit',
            field=models.ForeignKey(related_name='produit_vendu_produit', to='base.Produit'),
        ),
        migrations.AlterField(
            model_name='table',
            name='zone',
            field=models.ForeignKey(related_name='table_area', to='base.Zone'),
        ),
    ]
