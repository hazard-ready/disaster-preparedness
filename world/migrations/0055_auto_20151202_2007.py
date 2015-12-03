# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0054_auto_20151202_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='area_name',
            field=models.CharField(help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", max_length=100, default='the affected area'),
        ),
    ]
