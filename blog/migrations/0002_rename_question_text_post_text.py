# Generated by Django 4.0.3 on 2022-03-26 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='question_text',
            new_name='text',
        ),
    ]
