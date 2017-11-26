# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-23 00:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_datasource_estimated_records'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('download_by', models.CharField(max_length=150)),
                ('download_date', models.DateField(default=datetime.date.today)),
                ('scrape_script', models.CharField(max_length=150)),
                ('datasource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.DataSource')),
            ],
        ),
    ]
