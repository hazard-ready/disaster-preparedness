# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0024_snugget_tsunami_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnuggetSubSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snugget',
            name='sub_section',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True, to='world.SnuggetSubSection'),
            preserve_default=False,
        ),
    ]
