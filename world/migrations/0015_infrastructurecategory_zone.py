# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0014_auto_20150326_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='infrastructurecategory',
            name='zone',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, to='world.ImpactZone', default=1),
            preserve_default=False,
        ),
    ]
