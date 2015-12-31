# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0025_auto_20150328_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='sub_section',
            field=models.ForeignKey(to='world.SnuggetSubSection', on_delete=django.db.models.deletion.PROTECT, related_name='+', null=True),
            preserve_default=True,
        ),
    ]
