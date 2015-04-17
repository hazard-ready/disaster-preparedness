# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0045_textsnugget_snugget_ptr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.ForeignKey(to='world.Snugget', db_column='snugget_ptr', null=True),
            preserve_default=True,
        ),
    ]
