# Generated by Django 3.1 on 2020-09-20 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
        ('ecommerce', '0019_auto_20200919_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='item',
        ),
        migrations.RemoveField(
            model_name='variationimage',
            name='variation',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.variation'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
        migrations.DeleteModel(
            name='VariationImage',
        ),
    ]