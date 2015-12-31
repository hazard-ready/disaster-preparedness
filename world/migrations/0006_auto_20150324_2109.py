# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_auto_20150324_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactzone',
            name='feature',
            field=models.ForeignKey(to='world.ImpactZoneClass'),
            preserve_default=True,
        ),
    ]
