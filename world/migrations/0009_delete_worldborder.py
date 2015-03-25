# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0008_auto_20150325_2213'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WorldBorder',
        ),
    ]
