# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0005_auto_20210308_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabelFoundingArtist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artist', models.ForeignKey(related_name='+', blank=True, to='alibrary.Artist', null=True)),
                ('label', models.ForeignKey(related_name='+', blank=True, to='alibrary.Label', null=True)),
            ],
            options={
                'verbose_name': 'Founding Artist',
                'verbose_name_plural': 'Founding Artists',
            },
        ),
        migrations.AddField(
            model_name='label',
            name='founding_artists',
            field=models.ManyToManyField(related_name='founded_labels', verbose_name='Founder', to='alibrary.Artist', through='alibrary.LabelFoundingArtist', blank=True),
        ),
    ]
