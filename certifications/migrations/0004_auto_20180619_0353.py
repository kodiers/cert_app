# Generated by Django 2.0.6 on 2018-06-19 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifications', '0003_auto_20170811_0107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='certification',
        ),
        migrations.AddField(
            model_name='exam',
            name='certification',
            field=models.ManyToManyField(related_name='exams', to='certifications.Certification', verbose_name='Certification'),
        ),
    ]
