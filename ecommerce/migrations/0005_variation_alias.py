# Generated by Django 3.1 on 2020-08-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20200821_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='alias',
            field=models.CharField(blank=True, max_length=150, unique=True),
        ),
    ]
