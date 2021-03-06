# Generated by Django 4.0.6 on 2022-07-19 20:48

from django.db import migrations
import streams.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_blogdetailpage_created_at_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='banner_cta',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='content',
        ),
        migrations.AlterField(
            model_name='blogdetailpage',
            name='content',
            field=wagtail.fields.StreamField([('full_richtext', streams.blocks.RichTextBlock())], blank=True, null=True, use_json_field=None),
        ),
    ]
