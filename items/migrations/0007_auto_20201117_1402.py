# Generated by Django 3.1 on 2020-11-17 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201006_1437'),
        ('items', '0006_itemreview_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemreview',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.customer'),
        ),
    ]