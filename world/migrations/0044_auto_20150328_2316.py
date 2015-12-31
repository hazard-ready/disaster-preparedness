# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0043_auto_20150328_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactzonedata',
            name='area',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='orbndy24',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='orbndy24i',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='perimeter',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='subjstate',
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='shape_area',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='shape_leng',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='zone',
            field=models.CharField(max_length=10, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='zoneid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
