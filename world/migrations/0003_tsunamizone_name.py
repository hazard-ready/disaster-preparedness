# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_tsunamizone'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsunamizone',
            name='name',
            field=models.CharField(default=None, max_length=80),
            preserve_default=False,
        ),
    ]
