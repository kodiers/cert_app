# Generated by Django 2.2.6 on 2019-10-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parserconfig',
            name='certification_title_css_class',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Certification title css class'),
        ),
    ]
