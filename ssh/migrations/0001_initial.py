# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-02 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=100)),
                ('host_ip', models.CharField(max_length=100)),
                ('host_port', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('passwd', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssh.HostGroup')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssh.HostGroup'),
        ),
    ]