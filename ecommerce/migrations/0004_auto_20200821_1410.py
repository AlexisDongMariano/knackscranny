# Generated by Django 3.1 on 2020-08-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_auto_20200821_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
