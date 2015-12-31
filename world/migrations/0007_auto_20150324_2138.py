# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0006_auto_20150324_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactzone',
            name='feature',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ImpactZoneClass',
        ),
    ]
