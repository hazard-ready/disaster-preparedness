# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0004_auto_20150324_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactzone',
            name='feature',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impactzoneclass',
            name='desc',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
