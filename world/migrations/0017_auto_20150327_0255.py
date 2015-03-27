# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0016_auto_20150327_0231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snugget',
            name='impact_zone_filter',
        ),
        migrations.AddField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
