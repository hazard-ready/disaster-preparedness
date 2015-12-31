# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0049_embedsnugget'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snugget',
            name='type',
        ),
        migrations.AlterField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
