# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('like', models.IntegerField()),
            ],
            options={
                'db_table': 'advert',
            },
            bases=(models.Model,),
        ),
    ]
