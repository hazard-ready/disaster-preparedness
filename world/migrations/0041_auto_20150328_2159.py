# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0040_auto_20150328_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactzonedata',
            name='zone',
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='area',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='feature',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='orbndy24',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='orbndy24i',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='perimeter',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='subjstate',
            field=models.CharField(max_length=50, default=None),
            preserve_default=False,
        ),
    ]
