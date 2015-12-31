# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0047_auto_20150417_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textsnugget',
            name='id',
        ),
        migrations.AlterField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.OneToOneField(to='world.Snugget', primary_key=True, auto_created=True, parent_link=True, serialize=False),
            preserve_default=True,
        ),
    ]
