# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('advert', models.ForeignKey(to='advert.Advert')),
            ],
            options={
                'db_table': 'comments',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='advert',
            name='like',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterModelTable(
            name='advert',
            table='adverts',
        ),
    ]
