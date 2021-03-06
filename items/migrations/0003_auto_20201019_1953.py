# Generated by Django 3.1 on 2020-10-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20201018_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_label',
            field=models.CharField(choices=[('NA', 'Not Applicable'), ('NW', 'New'), ('SD', 'Sold'), ('BS', 'Bestseller'), ('SL', 'Sale')], default='NA', max_length=2),
        ),
        migrations.AlterField(
            model_name='variation',
            name='item_label',
            field=models.CharField(choices=[('NA', 'Not Applicable'), ('NW', 'New'), ('SD', 'Sold'), ('BS', 'Bestseller'), ('SL', 'Sale')], max_length=2),
        ),
    ]
