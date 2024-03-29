# Generated by Django 4.1.4 on 2023-09-04 04:31

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_projectpost_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpost',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=True),
        ),
    ]
