# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0050_auto_20150430_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(blank=True, editable=False, null=True),
            preserve_default=True,
        ),
    ]
