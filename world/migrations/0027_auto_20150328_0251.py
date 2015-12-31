# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0026_auto_20150328_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='sub_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, blank=True, related_name='+', to='world.SnuggetSubSection'),
            preserve_default=True,
        ),
    ]
