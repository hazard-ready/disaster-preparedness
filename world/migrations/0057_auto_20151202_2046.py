# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0056_auto_20151202_2027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactzonedata',
            name='shape_area',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='shape_leng',
        ),
    ]
