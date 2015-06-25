# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0051_auto_20150430_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snugget',
            name='tsunami_filter',
        ),
        migrations.DeleteModel(
            name='TsunamiZone',
        ),
    ]
