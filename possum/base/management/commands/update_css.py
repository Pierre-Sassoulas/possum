#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from possum.base.views.carte.categories import update_colors


class Command(BaseCommand):
    args = ""
    help = "Update CSS file for category"

    def handle(self, *args, **options):
        self.stdout.write("Colors updated")
        update_colors()

