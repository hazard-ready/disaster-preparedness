# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0042_auto_20150328_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsunamizone',
            name='type',
            field=models.CharField(max_length=50, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsunamizone',
            name='typeid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='tsunamizone',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='scenario_type',
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='scenario_id',
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='location',
        ),
    ]
