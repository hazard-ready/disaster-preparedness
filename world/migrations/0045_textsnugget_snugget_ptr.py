# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0044_auto_20150328_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.ForeignKey(db_column='base_ptr', null=True, to='world.Snugget'),
            preserve_default=True,
        ),
    ]
