# Generated by Django 4.0.5 on 2022-07-04 04:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_remove_blogdetailpage_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='blogdetailpage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
