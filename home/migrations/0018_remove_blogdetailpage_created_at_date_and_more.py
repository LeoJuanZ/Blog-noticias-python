# Generated by Django 4.0.5 on 2022-07-04 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_rename_created_at_order_blogdetailpage_created_at_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='created_at_date',
        ),
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='created_at_date_time',
        ),
    ]
