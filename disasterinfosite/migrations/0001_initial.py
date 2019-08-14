# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import embed_video.fields
import django.db.models.deletion
import django.contrib.gis.db.models.fields

from disasterinfosite.models import OverwriteStorage

class Migration(migrations.Migration):
    operations = [
            migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('about_text', models.TextField(default='Information about your organization goes here.', help_text='Describe the data and the agencies that it came from.')),
                ('contact_email', models.EmailField(blank=True, help_text='Put a contact email for the maintainer of this site here.', max_length=254)),
                ('site_url', models.URLField(default='https://www.example.com', help_text='Put the URL to this site here.')),
                ('site_title', models.CharField(default='Your Title Here!', max_length=50)),
                ('site_description', models.CharField(default='A disaster preparedness website', help_text='A small, catchy description for this site.', max_length=200)),
                ('data_download', models.URLField(help_text='A link where people can download a zipfile of all the data that powers this site.', blank=True)),
                ('intro_text', models.TextField(help_text='A description of what we are trying to help people prepare for, or the goal of your site.', default='A natural disaster could strike your area at any time.')),
                ('who_made_this', models.TextField(help_text='Include information about who you are and how to contact you.', default='Information about the creators and maintainers of this particular site.')),
                ('area_name', models.CharField(default='the affected area', help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", max_length=100)),

            ],
            options={
                'verbose_name': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Location Information'
            },
        ),
        migrations.CreateModel(
            name='ShapefileGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=50, default="")),
                ('order_of_appearance', models.IntegerField(help_text='The order, from top to bottom, in which you would like this group to appear, when applicable.', default=0)),
                ('note', models.TextField(blank=True, help_text='A note that appears above all snuggets in this section. Use for data caveats or warnings.')),
            ],
        ),
        migrations.CreateModel(
            name='SnuggetType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('model_name', models.CharField(choices=[('SNUG_TEXT', 'TextSnugget')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SnuggetSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('display_name', models.CharField(default="", help_text='The name to show for this section', max_length=50)),
                ('collapsible', models.BooleanField(default=True, help_text='Whether this section of the data is collapsible')),
                ('order_of_appearance', models.IntegerField(default=0, help_text="The order in which you'd like this to appear in the tab. 0 is at the top."))
            ],
        ),
         migrations.CreateModel(
            name='SnuggetPopOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text',models.TextField(default='', max_length=255)),
                ('image', models.ImageField(upload_to='popout_images')),
                ('link', models.TextField(default='', max_length=255)),
                ('text', models.TextField(default='')),
                ('video', embed_video.fields.EmbedVideoField(null=True))
            ],
        ),
        migrations.CreateModel(
            name='Snugget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('percentage', models.FloatField(null=True)),
                ('section', models.ForeignKey(to='disasterinfosite.SnuggetSection', on_delete=models.PROTECT, related_name='+')),
                ('group', models.ForeignKey(to='disasterinfosite.ShapefileGroup', null=True, on_delete=models.PROTECT)),
                ('pop_out', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='disasterinfosite.SnuggetPopOut')),
                ('order', models.IntegerField(default=0))
            ],
        ),
        migrations.CreateModel(
            name='TextSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, to='disasterinfosite.Snugget', serialize=False, primary_key=True, parent_link=True, on_delete=models.CASCADE)),
                ('content', models.TextField()),
            ],
            bases=('disasterinfosite.snugget',),
        ),
        migrations.CreateModel(
            name='PreparednessAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('image', models.ImageField(upload_to='prepare_images')),
                ('cost', models.IntegerField(default=0, validators=[django.contrib.postgres.validators.RangeMinValueValidator(0), django.contrib.postgres.validators.RangeMaxValueValidator(4)])),
                ('happy_text', models.TextField(default='')),
                ('useful_text', models.TextField(default='')),
                ('property_text', models.TextField(default='')),
                ('content_text', models.TextField(default='')),
                ('link_text', models.TextField(default='')),
                ('link_icon', models.ImageField(upload_to='prepare_images')),
                ('link', models.URLField(default='')),
                ('slug', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(blank=True, max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('zip_code', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('actions_taken', models.ManyToManyField(to='disasterinfosite.PreparednessAction')),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
        migrations.CreateModel(
            name='SnuggetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('model_name', models.CharField(choices=[('SNUG_TEXT', 'TextSnugget'), ('SNUG_VIDEO', 'EmbedSnugget'), ('SNUG_SLIDESHOW', 'SlideshowSnugget')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DataOverviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_text', models.CharField(default='', max_length=100)),
                ('image', models.ImageField(storage=disasterinfosite.models.OverwriteStorage(), upload_to='data')),
                ('link_text_es', models.CharField(default='', max_length=100, null=True)),
                ('link_text_en', models.CharField(default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmbedSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, to='disasterinfosite.Snugget', serialize=False, primary_key=True, parent_link=True, on_delete=models.CASCADE)),
                ('video', embed_video.fields.EmbedVideoField()),
                ('text', models.TextField(default='')),
            ],
            bases=('disasterinfosite.snugget',),
        ),
        migrations.CreateModel(
            name='SlideshowSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='disasterinfosite.Snugget')),
                ('text', models.TextField(default='')),
            ],
            bases=('disasterinfosite.snugget',),
        ),
        migrations.CreateModel(
            name='PastEventsPhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('snugget', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='disasterinfosite.SlideshowSnugget')),
                ('image', models.ImageField(upload_to='photos')),
                ('caption', models.TextField(default="", max_length=200))
            ],
        ),
         migrations.CreateModel(
            name='DataOverviewImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('link_text', models.CharField(max_length=100, default='')),
                ('image', models.ImageField(storage=OverwriteStorage(), upload_to='data')),
            ],
        ),
        migrations.AlterField(
            model_name='snuggettype',
            name='model_name',
            field=models.CharField(choices=[('SNUG_TEXT', 'TextSnugget'), ('SNUG_VIDEO', 'EmbedSnugget'), ('SNUG_SLIDESHOW', 'SlideshowSnugget')], max_length=255),
        ),
    ]
