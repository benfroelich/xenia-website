# Generated by Django 4.1 on 2022-09-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsblog', '0007_comment_edits_alter_comment_first_published_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
