# Generated by Django 4.0.5 on 2022-07-03 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_homepage_banner_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.AlterModelOptions(
            name='blogdetailpage',
            options={'verbose_name': 'Pagina de noticia', 'verbose_name_plural': 'Pagina de noticias'},
        ),
    ]
