# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0055_auto_20151202_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Location Information'},
        ),
        migrations.AlterField(
            model_name='location',
            name='area_name',
            field=models.CharField(max_length=100, help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", default='The affected area'),
        ),
    ]
