# Generated by Django 4.1 on 2022-09-01 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsblog', '0004_remove_blogpost_author_remove_comment_author_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='user',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]