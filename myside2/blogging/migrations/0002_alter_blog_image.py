# Generated by Django 4.2.13 on 2024-08-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
