# Generated by Django 3.1 on 2020-08-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_auto_20200823_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationimage',
            name='name',
            field=models.CharField(default='regular', max_length=100, unique=True),
        ),
    ]
