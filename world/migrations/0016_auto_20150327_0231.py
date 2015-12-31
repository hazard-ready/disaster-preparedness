# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0015_infrastructurecategory_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snugget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('impact_zone_filter', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnuggetSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnuggetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('model_name', models.CharField(max_length=255, choices=[('SNUG_TEXT', 'TextSnugget')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextSnugget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snugget',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.SnuggetSection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='shaking_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.ExpectedGroundShaking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.SnuggetType'),
            preserve_default=True,
        ),
    ]
