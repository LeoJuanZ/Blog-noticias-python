# Generated by Django 4.0.5 on 2022-07-04 17:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_blogdetailpage_publication_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailpage',
            name='created_at_order',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
