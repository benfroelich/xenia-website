# Generated by Django 4.2.4 on 2023-09-01 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_stats_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statcategory',
            name='units',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='stats',
            name='details',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
