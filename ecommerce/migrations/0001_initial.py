# Generated by Django 3.1 on 2020-08-21 13:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='regular', max_length=100)),
                ('price', models.FloatField()),
                ('price_discount', models.FloatField(blank=True, null=True)),
                ('description', models.TextField()),
                ('inventory', models.PositiveIntegerField(blank=True, default=0)),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.item')),
            ],
        ),
    ]
